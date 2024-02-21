from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from dotenv import load_dotenv

import logging
import string
import random
import time
import os

from modules import generate_short_url, wait_for_url

app = Flask(__name__,template_folder='templates')
# Load Environment Variables
load_dotenv()
# Configure Database
mongo_url = os.getenv("MONGO_DB_URL")
client = MongoClient(mongo_url)
db = client['url_app']
collection = db['url']
contacts = db['contacts']
subscribers = db['subscribers']
# Configure Logging Format
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='logs/app.log',
                    filemode='w',
                    level=logging.INFO)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        contact_user_name = request.form['contact_user_name']
        contact_email = request.form['contact_email']
        contact_message = request.form['contact_message']
        contacts.insert_one({"contact_user_name": contact_user_name,"contact_email":contact_email,"contact_message":contact_message})       
    
    return render_template('index.html')



@app.route("/subscribe", methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        subscribe_mail = request.form['subscribe_mail']
        subscribers.insert_one({"email": subscribe_mail})
    return redirect('/')

@app.route("/<short_url>")
def redirect_url(short_url):
    short_url_doc = collection.find_one({"short_url": short_url})
    if short_url_doc:
        long_url = short_url_doc["long_url"]
        # Uncomment this if you want to redirect in page
        #return render_template('pages/redirect.html',long_url=long_url)
        return redirect(long_url)
    else:
        return render_template('pages/404.html'), 404


@app.route("/links")
def show_links():
    all_links = collection.find()
    url_domain = str(request.url_root)
    return render_template('pages/links.html',all_links=all_links,url_domain=url_domain)

@app.route("/display", methods=["GET", "POST"])
def display():
    if request.method == "POST":
        long_url = request.form["long_url"]
        if long_url != "":
            short_url_doc = collection.find_one({"long_url": long_url})
            if short_url_doc:
                short_url = short_url_doc["short_url"]
            else:
                short_url = generate_short_url()
                while collection.find_one({"short_url": short_url}):
                    short_url = generate_short_url()
                
                collection.insert_one({"short_url": short_url, "long_url": long_url})
                logging.info(f' - Created {short_url} for {long_url} ')
                
            full_url = request.url_root + short_url
            return render_template('pages/display.html', short_url=short_url, full_url=full_url)
        else:
            return render_template('index.html')        
    return render_template('index.html')


@app.route('/log')
def display_logs():
    log_entries = read_log_file('logs/app.log')
    return render_template('pages/log.html', log_entries=log_entries)

def read_log_file(file_path):
    with open(file_path, 'r') as file:
        log_entries = [line.strip() for line in file.readlines() if not line.startswith('#')]
    return log_entries

#404
@app.errorhandler(404)
def page_404(error):
    return render_template('pages/404.html'), 404


if __name__ == '__main__':
    app.run(debug=False, port=5000)
