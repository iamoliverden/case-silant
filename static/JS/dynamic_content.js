// static/js/dynamic_content.js

// Phone number and app name
const phoneNumber = '+7 (8352) 201209';
const appName = 'My Silant 2022';

// Update the phone number in the HTML
document.addEventListener('DOMContentLoaded', () => {
    console.log('dynamic_content.js loaded');

    const phoneNumberElement = document.getElementById('phone-number');
    const footerPhoneNumberElement = document.getElementById('footer-phone-number');
    const footerAppNameElement = document.getElementById('footer-app-name');

    if (phoneNumberElement) {
        phoneNumberElement.textContent = phoneNumber;
    } else {
        console.log('Element with ID "phone-number" not found');
    }

    if (footerPhoneNumberElement) {
        footerPhoneNumberElement.textContent = phoneNumber;
    } else {
        console.log('Element with ID "footer-phone-number" not found');
    }

    if (footerAppNameElement) {
        footerAppNameElement.textContent = appName;
    } else {
        console.log('Element with ID "footer-app-name" not found');
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
    } else {
        console.log('Element with ID "logo" or "is-logged-in" not found');
    }
});
