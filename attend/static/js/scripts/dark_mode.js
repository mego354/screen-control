// Load dark mode preference on page load
document.addEventListener('DOMContentLoaded', () => {
    const darkMode = localStorage.getItem('darkMode') === 'true';
    const dark_icon = document.getElementById('dark_icon');

    // Apply dark mode and corresponding root variables if previously enabled
    if (darkMode) {
        document.body.classList.add('dark-mode');
        setDarkModeVariables();
        dark_icon.classList.remove('fa-sun');
        dark_icon.classList.add('fa-moon');
    } else {
        setLightModeVariables();
        dark_icon.classList.remove('fa-moon');
        dark_icon.classList.add('fa-sun');
    }
});

// Dark Mode Toggle
document.getElementById('toggle-contrast').addEventListener('click', function () {
    const darkModeEnabled = document.body.classList.toggle('dark-mode');
    
    // Save the current dark mode state in localStorage
    localStorage.setItem('darkMode', darkModeEnabled);
    
    const dark_icon = document.getElementById('dark_icon');
    
    // Update the icon and CSS variables based on dark mode state
    if (darkModeEnabled) {
        setDarkModeVariables();
        dark_icon.classList.remove('fa-sun');
        dark_icon.classList.add('fa-moon');
    } else {
        setLightModeVariables();
        dark_icon.classList.remove('fa-moon');
        dark_icon.classList.add('fa-sun');
    }
});

// Function to apply dark mode variables
function setDarkModeVariables() {
    const root = document.documentElement;

    root.style.setProperty('--bs-white', '#1a1a1a');
    root.style.setProperty('--bs-black', '#fff');
    root.style.setProperty('--bs-gray', '#f8f9fa');
    root.style.setProperty('--bs-light', '#343a40');
    root.style.setProperty('--bs-trans-light', '#343a40d0');
}

// Function to apply light mode variables
function setLightModeVariables() {
    const root = document.documentElement;

    root.style.setProperty('--bs-white', '#fff');
    root.style.setProperty('--bs-black', '#1a1a1a');
    root.style.setProperty('--bs-gray', '#343a40');
    root.style.setProperty('--bs-light', '#f8f9fa');
    root.style.setProperty('--bs-trans-light', '#f5f5f5cc');
}
