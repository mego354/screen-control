document.addEventListener('DOMContentLoaded', function() {
    // Limit input for username field to 7 digits, allowing only numeric characters
    document.getElementById('id_user_name').oninput = function() {
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
    // Limit input for nationa ID field to 14 digits, allowing only numeric characters
    document.getElementById('id_national_id').oninput = function() {
        // Retrieve the current value of the input field
        let national_idInput = this.value;

        // Remove any non-digit characters
        national_idInput = national_idInput.replace(/\D/g, '');

        // Limit the input to a maximum of 14 digits
        if (national_idInput.length > 14) {
            national_idInput = national_idInput.slice(0, 14);
        }

        // Update the input field with the sanitized value
        this.value = national_idInput;
    };



    const form = document.getElementById('registration-form');
    const userNameField = form.user_name;
    const nationalIdField = form.national_id;
    const emailField = form.email;
    const passwordField = form.password;
    const confirmPasswordField = form.confirm_password;

    form.addEventListener('submit', function(event) {
        // Clear previous error messages

        clearErrors();

        // Validate fields
        let valid = true;

        // Validate username
        if (!validateUserName(userNameField.value)) {
            showError('user_name_error', 'Academic ID must be numeric, at least 6 digits, and start with 22, 23, or 24.');
            valid = false;
        }

        // Validate national ID
        if (!validateNationalId(nationalIdField.value)) {
            showError('national_id_error', 'National ID must be exactly 14 digits long.');
            valid = false;
        }

        // Validate email
        if (!validateEmail(emailField.value)) {
            showError('email_error', 'Invalid email format.');
            valid = false;
        }

        // Validate password
        if (passwordField.value.length < 6) {
            showError('password_error', 'Password must be at least 6 characters long.');
            valid = false;
        }

        // Confirm password
        if (passwordField.value !== confirmPasswordField.value) {
            showError('confirm_password_error', 'Passwords do not match.');
            valid = false;
        }

        // Prevent form submission if invalid
        if (!valid) {
            event.preventDefault();
        }
    });

    function clearErrors() {
        document.getElementById('user_name_error').parentElement.classList.add('hidden');
        document.getElementById('national_id_error').parentElement.classList.add('hidden');
        document.getElementById('email_error').parentElement.classList.add('hidden');
        document.getElementById('password_error').parentElement.classList.add('hidden');
        document.getElementById('confirm_password_error').parentElement.classList.add('hidden');
    }

    function showError(elementId, message) {
        var li = document.getElementById(elementId);
        li.innerText = message;
        li.parentElement.classList.remove('hidden')

    }

    function validateUserName(username) {
        const regex = /^[a-zA-Z0-9_]{6,}$/; // Only alphanumeric characters and underscores, minimum 6 characters
        return regex.test(username);
    }

    function validateNationalId(nationalId) {
        return /^\d{14}$/.test(nationalId); // Exactly 14 digits
    }

    function validateEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Basic email validation
        return regex.test(email);
    }
});