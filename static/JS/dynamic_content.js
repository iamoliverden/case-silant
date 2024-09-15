// static/js/dynamic_content.js

// Phone number and app name
const phoneNumber = '+7 (8352) 201209';
const appName = 'My Silant 2022';

// Update the phone number in the HTML
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('phone-number').textContent = phoneNumber;
    document.getElementById('footer-phone-number').textContent = phoneNumber;
    document.getElementById('app-name').textContent = appName;
    document.getElementById('footer-app-name').textContent = appName;
});
