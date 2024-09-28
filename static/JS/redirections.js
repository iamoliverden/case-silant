// static/js/redirections.js

document.addEventListener('DOMContentLoaded', () => {
    const generalInfo = document.getElementById('general-info');
    const technicalMaintenance = document.getElementById('technical-maintenance');
    const claims = document.getElementById('claims');

    if (generalInfo) {
        generalInfo.addEventListener('click', function() {
            window.location.href = window.location.origin + '/logged_in/';
        });
    }

    if (technicalMaintenance) {
        technicalMaintenance.addEventListener('click', function() {
            window.location.href = window.location.origin + '/technical_maintenance/';
        });
    }

    if (claims) {
        claims.addEventListener('click', function() {
            window.location.href = window.location.origin + '/claims/';
        });
    }
});
