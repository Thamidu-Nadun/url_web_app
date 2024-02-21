import string
import random
import time
from flask import render_template

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url


def wait_for_url():
    time.sleep(2000)
    return render_template('index.html')
if __name__ == "__main__":
    def main():
        generate_short_url()