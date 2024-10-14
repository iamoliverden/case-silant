    document.addEventListener("DOMContentLoaded", function() {
        if (!window.location.search) {
            // This condition prevents form submission if the form was already submitted and redirected back.
            document.getElementById("search-button").click();
        }
    });