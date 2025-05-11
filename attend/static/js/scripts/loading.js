document.addEventListener("DOMContentLoaded", function() {
    // Add a 0.5-second delay before hiding the spinner and showing the content and footer
    setTimeout(function() {
        // Hide the loading spinner
        document.querySelector(".loading_container").style.display = "none";
        
    }, 500); // 1000 milliseconds = 1 second
});
