// static/js/dynamic_content.js

// static/js/dynamic_content.js

// Phone number and app name
const phoneNumber = '+7 (8352) 201209';
const appName = 'My Silant 2022';

// Update the phone number in the HTML
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('phone-number').textContent = phoneNumber;
    document.getElementById('footer-phone-number').textContent = phoneNumber;
    document.getElementById('footer-app-name').textContent = appName;

    // Add click event listener to the logo
    const logo = document.getElementById('logo');
    const isLoggedIn = document.getElementById('is-logged-in').value === 'true';
    const loggedInUrl = logo.getAttribute('data-logged-in-url');
    const loggedOutUrl = logo.getAttribute('data-logged-out-url');

    logo.addEventListener('click', () => {
        if (isLoggedIn) {
            window.location.href = loggedInUrl;
        } else {
            window.location.href = loggedOutUrl;
        }
    });
});
