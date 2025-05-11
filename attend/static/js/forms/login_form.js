// Limit input for username field to 7 digits, allowing only numeric characters
document.getElementById('id_username').oninput = function() {
    // Retrieve the current value of the input field
    let usernameInput = this.value;

    // Remove any non-digit characters
    usernameInput = usernameInput.replace(/\D/g, '');

    // Limit the input to a maximum of 7 digits
    if (usernameInput.length > 7) {
        usernameInput = usernameInput.slice(0, 7);
    }

    // Update the input field with the sanitized value
    this.value = usernameInput;
};

// Limit input for password field to a maximum of 30 characters
document.getElementById('id_password').oninput = function() {
    // Retrieve the current value of the input field
    let passwordInput = this.value;

    // Limit the input to a maximum of 30 characters
    if (passwordInput.length > 30) {
        passwordInput = passwordInput.slice(0, 30);
    }

    // Update the input field with the trimmed value
    this.value = passwordInput;
};

// Form submission event listener for validation
document.getElementById('loginForm').addEventListener('submit', function(event) {
    // Retrieve and trim the username and password values
    const username = this.username.value.trim();
    let isValid = true;

    // Clear previous error messages
    const errorMessages = document.querySelectorAll('.text-danger');
    errorMessages.forEach(function(msg) {
        msg.innerHTML = '';
    });

    // Validate the username input
    if (username.length < 6 || !/^(22|23|24)/.test(username)) {
        isValid = false;
        console.log(!/^(22|23|24)\d{7}$/.test(username))
        const usernameError = document.createElement('div');
        usernameError.classList.add('text-danger');
        usernameError.innerHTML = 'Academic ID must be numeric, at least 6 digits, and start with 22, 23, or 24.';
        this.username.parentNode.appendChild(usernameError);
    }

    // If the form is not valid, prevent submission
    if (!isValid) {
        event.preventDefault();
    }
});
