// Function to get URL parameters
function getUrlParams() {
    return new URLSearchParams(window.location.search);
}

// Function to update or add a URL parameter
function updateUrlParam(param, value) {
    const params = getUrlParams();

    // Update the param or add it if it doesn't exist
    if (value) {
        params.set(param, value);
    } else {
        params.delete(param); // Remove the parameter if value is empty
    }

    // Reset page parameter to 1 when updating selections
    params.set('page', '1');

    // Construct the new URL with updated parameters
    return `${window.location.protocol}//${window.location.host}${window.location.pathname}?${params.toString()}`;
}

// Function to handle input changes (select, radio, date)
function handleInputChange(inputIdOrName, paramName, inputType = 'select') {
    let inputElement;

    if (inputType === 'radio') {
        inputElement = document.querySelector(`input[name="${inputIdOrName}"]:checked`);
    } else {
        inputElement = document.getElementById(inputIdOrName);
    }

    if (!inputElement) return console.log('Element not found'); // Prevent errors if element not found

    if (inputType === 'radio') {
        const radioElements = document.querySelectorAll(`input[name="${inputIdOrName}"]`);
        radioElements.forEach(radio => {
            radio.addEventListener('change', function() {
                const selectedValue = this.value;
                const newUrl = updateUrlParam(paramName, selectedValue);
                window.location.href = newUrl;
            });
        });

        // Preselect based on URL params when the page loads
        const params = getUrlParams();
        const preselectValue = params.get(paramName);
        const radioElement = document.querySelector(`input[name="${paramName}"][value="${preselectValue}"]`);
        if (radioElement) radioElement.checked = true;
    } else {
        inputElement.addEventListener('change', function() {
            const selectedValue = this.value;
            const newUrl = updateUrlParam(paramName, selectedValue);
            window.location.href = newUrl;
        });

        // Preselect based on URL params when the page loads
        const params = getUrlParams();
        const preselectValue = params.get(paramName);
        if (inputType === 'select' && preselectValue) {
            inputElement.value = preselectValue;
        } else if (inputType === 'date' && preselectValue) {
            inputElement.value = preselectValue;
        }
    }
}

// Function to reset all filters (clear URL params)
function resetFilters() {
    const baseUrl = `${window.location.protocol}//${window.location.host}${window.location.pathname}`;
    window.location.href = baseUrl; // Redirect to the base URL, clearing all parameters
}

// Initialize filters on page load
function initializeFilters() {
    // Handle select filters
    const selectFilters = [
        { id: 'filter-college', param: 'college' },
        { id: 'filter-department', param: 'department' },
        { id: 'filter-year', param: 'year' },
        { id: 'filter-group', param: 'group' },
        { id: 'filter-class', param: 'class' },
        { id: 'filter-room', param: 'room' },
        { id: 'filter-course', param: 'course' },
        { id: 'filter-doctor', param: 'doctor' },
        { id: 'filter-day', param: 'day' },  // New Day of the Week filter
    ];

    selectFilters.forEach(filter => handleInputChange(filter.id, filter.param, 'select'));

    // Handle radio button filters
    const radioFilters = [
        { name: 'events_type', param: 'events_type' },
        { name: 'standard', param: 'standard' }
    ];

    radioFilters.forEach(filter => handleInputChange(filter.name, filter.param, 'radio'));

    // Handle date filters
    const dateFilters = [
        { id: 'filter-start-date', param: 'start_date' },
        { id: 'filter-end-date', param: 'end_date' }
    ];

    dateFilters.forEach(filter => handleInputChange(filter.id, filter.param, 'date'));

    // Add event listener to reset button
    document.getElementById('reset-filters').addEventListener('click', resetFilters);
}

// Call initializeFilters when the page loads
window.onload = initializeFilters;
