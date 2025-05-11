document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('password-reset-form');
    const submitButton = document.getElementById('submit-button');
    
    // Check if there's a stored time in localStorage
    const lastRequestTime = localStorage.getItem('lastPasswordResetRequest');
    
    // If there is, calculate the time left until the button can be re-enabled
    if (lastRequestTime) {
        const timePassed = Date.now() - lastRequestTime;
        const timeLeft = 60000 - timePassed; // 1 minute in milliseconds
        
        if (timeLeft > 0) {
            // Disable the button and show remaining time
            submitButton.disabled = true;
            submitButton.textContent = `Please wait... (${Math.ceil(timeLeft / 1000)}s left)`;

            // Start a countdown
            const countdownInterval = setInterval(() => {
                const timeLeft = 60000 - (Date.now() - lastRequestTime);
                
                if (timeLeft <= 0) {
                    // Re-enable the button
                    submitButton.disabled = false;
                    submitButton.textContent = 'Reset Password';
                    clearInterval(countdownInterval);
                } else {
                    // Update button text with remaining time
                    submitButton.textContent = `Please wait... (${Math.ceil(timeLeft / 1000)}s left)`;
                }
            }, 1000);
        }
    }

    form.addEventListener('submit', function(event) {
        // Store the current time in localStorage
        localStorage.setItem('lastPasswordResetRequest', Date.now());

        // Disable the submit button immediately
        submitButton.disabled = true;
        submitButton.textContent = 'Please wait... (60s left)';

        // Start the countdown for 60 seconds
        const countdownInterval = setInterval(() => {
            const timeLeft = 60000 - (Date.now() - lastRequestTime);
            
            if (timeLeft <= 0) {
                // Re-enable the button
                submitButton.disabled = false;
                submitButton.textContent = 'Reset Password';
                clearInterval(countdownInterval);
            } else {
                // Update button text with remaining time
                submitButton.textContent = `Please wait... (${Math.ceil(timeLeft / 1000)}s left)`;
            }
        }, 1000);
    });
});
