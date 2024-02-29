// Add your JavaScript code here

// Function to dynamically generate form fields based on selected category
function generateFormFields(category) {
    const formFieldsDiv = document.getElementById('form-fields');
    formFieldsDiv.innerHTML = ''; // Clear existing form fields

    switch(category) {
        case 'food':
            formFieldsDiv.innerHTML = `
                <input type="text" id="name" placeholder="Name">
                <input type="text" id="food-quantity" placeholder="Food Quantity">
                <input type="date" id="expiry-date">
                <textarea id="description" placeholder="Description"></textarea>
            `;
            break;
        case 'clothes':
            formFieldsDiv.innerHTML = `
                <input type="text" id="name" placeholder="Name">
                <input type="text" id="clothing-type" placeholder="Clothing Type">
                <input type="text" id="gender" placeholder="Gender">
                <input type="text" id="clothing-size" placeholder="Clothing Size">
                <input type="text" id="condition" placeholder="Condition">
                <textarea id="description" placeholder="Description"></textarea>
            `;
            break;
        case 'groceries':
            formFieldsDiv.innerHTML = `
                <input type="text" id="name" placeholder="Name">
                <input type="text" id="quantity" placeholder="Quantity">
                <input type="date" id="expiry-date">
                <input type="time" id="expiry-time">
                <textarea id="description" placeholder="Description"></textarea>
            `;
            break;
        case 'toys':
            formFieldsDiv.innerHTML = `
                <input type="text" name="age-group" placeholder="Age Group">
                <input type="text" name="cond" placeholder="Condition">
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
