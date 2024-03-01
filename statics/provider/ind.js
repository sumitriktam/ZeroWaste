// Add your JavaScript code here


function generateFormFields(category) {
    const formFieldsDiv = document.getElementById('form-fields');
    formFieldsDiv.innerHTML = ''; 

    switch(category) {
        case 'food':
            formFieldsDiv.innerHTML = `
            <input type="date" name="expiry-date">
            <input type="time" name="expiry-time">
            <textarea name="desc" placeholder="Description"></textarea>
            `;
            break;
        case 'clothes':
            formFieldsDiv.innerHTML = `
                <input type="text" name="gender" placeholder="Gender">
                <input type="text" name="size" placeholder="Clothing Size">
                <input type="text" name="cond" placeholder="Condition">
                <textarea name="desc" placeholder="Description"></textarea>
            `;
            break;
        case 'groceries':
            formFieldsDiv.innerHTML = `
                <input type="date" name="expiry-date">
                <input type="time" name="expiry-time">
                <textarea name="desc" placeholder="Description"></textarea>
            `;
            break;
        case 'toys':
            formFieldsDiv.innerHTML = `
                <input type="text" name="age-group" placeholder="Age Group">
                <input type="text" name="cond" placeholder="Condition">
                <textarea name="desc" placeholder="Description"></textarea>
            `;
            break;
        case 'others':
                formFieldsDiv.innerHTML = `
                    <textarea name="desc" placeholder="Description"></textarea>
                `;
            break;
        default:
            // Do nothing
            break;
    }
}

// Event listener for category dropdown change
document.getElementById('category').addEventListener('change', function() {
    const selectedCategory = this.value;
    generateFormFields(selectedCategory);
});

// JavaScript for handling form submission (to be implemented)
document.getElementById('post-form').addEventListener('submit', function(event) {
    event.preventDefault();
    // Handle form submission (e.g., send data to server)
    // This will be implemented in your Django backend
});
