// static/js/dynamic_content.js

// Phone number and app name
const phoneNumber = '+7 (8352) 201209';
const appName = 'My Silant 2022';

// Update the phone number in the HTML
document.addEventListener('DOMContentLoaded', () => {
    const phoneNumberElement = document.getElementById('phone-number');
    const footerPhoneNumberElement = document.getElementById('footer-phone-number');
    const footerAppNameElement = document.getElementById('footer-app-name');

    if (phoneNumberElement) {
        phoneNumberElement.textContent = phoneNumber;
    }

    if (footerPhoneNumberElement) {
        footerPhoneNumberElement.textContent = phoneNumber;
    }

    if (footerAppNameElement) {
        footerAppNameElement.textContent = appName;
    }

    // Add click event listener to the logo
    const logo = document.getElementById('logo');
    const isLoggedInElement = document.getElementById('is-logged-in');

    if (logo && isLoggedInElement) {
        const isLoggedIn = isLoggedInElement.value === 'true';
        const loggedInUrl = logo.getAttribute('data-logged-in-url');
        const loggedOutUrl = logo.getAttribute('data-logged-out-url');

        logo.addEventListener('click', () => {
            if (isLoggedIn) {
                window.location.href = loggedInUrl;
            } else {
                window.location.href = loggedOutUrl;
            }
        });
    }
});
