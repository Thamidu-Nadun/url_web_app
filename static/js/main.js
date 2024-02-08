// nav bar
var menuIcon = document.querySelector('.fa-bars');
var navBar = document.querySelector('.nav_ul');
var navList = document.querySelector('.nav-list');

menuIcon.onclick = function() {
    if (menuIcon.classList.contains('fa-bars')) {
        menuIcon.classList.replace('fa-bars', 'fa-times');
        navBar.classList.add('expand');
        navList.classList.add('nav-list-show');
    } else {
        menuIcon.classList.replace('fa-times', 'fa-bars');
        navBar.classList.add('expand');
        navList.classList.remove('nav-list-show');
    }
};
