// JavaScript for header scroll effect and dark mode toggle
const header = document.getElementById('header');
const themeToggle = document.getElementById('theme-toggle');

window.addEventListener('scroll', function() {
    if (window.scrollY > 10) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

themeToggle.addEventListener('change', function() {
    document.body.classList.toggle('dark-mode');
});