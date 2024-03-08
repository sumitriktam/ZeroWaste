// Add your JavaScript code here
function generateFormFields(category) {
    const formFieldsDiv = document.getElementById('form-fields');
    formFieldsDiv.innerHTML = ''; 

    switch(category) {
        case 'food':
            formFieldsDiv.innerHTML = `
            <label for="expiry-date">Expiry Date:</label>
            <input type="date" name="expiry-date" style="width: 100%;padding: 8px;margin-bottom: 12px;border: 1px solid #ccc;border-radius: 5px;box-sizing: border-box;">
            
            
            <label for="expiry-time">Expiry Time:</label>
            <input type="time" id="expiry-time" name="expiry-time" class="form-input">
            <label for="desc">Description:</label>
            <textarea id="desc" name="desc" placeholder="Description" class="form-textarea"></textarea>
            `;
            break;
        case 'clothes':
            formFieldsDiv.innerHTML = `
            <label for="gender">Gender:</label>
            <input type="text" id="gender" name="gender" placeholder="Gender" class="form-input">
            <label for="size">Clothing Size:</label>
            <select id="size" name="size" class="form-input" required>
                <option value="s">S(Small)</option>
                <option value="m">M(Medium)</option>
                <option value="l">L(Large)</option>
                <option value="xl">XL(Extra Large)</option>
                <option value="xxl">M(2 Extra Large)</option>
                <option value="others">Others</option>
            
            </select>
            
            <label for="cond">Condition:</label>
            <select id="cond" name="cond" class="form-input" required>
                            <option value="new">New</option>
                            <option value="mint">Mint</option>
                            <option value="old">Old</option>
                            
            </select><br>
            
            <label for="desc">Description:</label>
            <textarea id="desc" name="desc" placeholder="Description" class="form-textarea"></textarea>
            `;
            break;
        case 'toys':
            formFieldsDiv.innerHTML = `
            <label for="age-group">Age Group:</label>
            <input type="text" id="age-group" name="age-group" placeholder="Age Group" class="form-input">
            <label for="cond">Condition:</label>
            <select id="cond" name="cond" class="form-input" required>
                            <option value="new">New</option>
                            <option value="mint">Mint</option>
                            <option value="old">Old</option>
                            
            </select>
            
            <label for="desc">Description:</label>
            <textarea id="desc" name="desc" placeholder="Description" class="form-textarea"></textarea>
            `;
            break;
        case 'groceries':
            formFieldsDiv.innerHTML = `
            <label for="expiry-date">Expiry Date:</label>
            <input type="date" id="expiry-date" name="expiry-date" class="form-input">
            <label for="expiry-time">Expiry Time:</label>
            <input type="time" id="expiry-time" name="expiry-time" class="form-input">
            <label for="desc">Description:</label>
            <textarea id="desc" name="desc" placeholder="Description" class="form-textarea"></textarea>
            `;
            break;
        case 'others':
            formFieldsDiv.innerHTML = `
            <label for="desc">Description:</label>
            <textarea id="desc" name="desc" placeholder="Description" class="form-textarea"></textarea>
            `;
            break;
        default:
            // Handle default case or do nothing
            break;
    }
}

function previewImage(event) {
    const preview = document.getElementById('previewImage');
    const fileInput = event.target;

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
        };

        reader.readAsDataURL(fileInput.files[0]);
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


        

// function generateFormFields(category) {
//     const formFieldsDiv = document.getElementById('form-fields');
//     formFieldsDiv.innerHTML = ''; 

//     switch(category) {
//         case 'food':
//             formFieldsDiv.innerHTML = `
//             <label for 
//             <input type="date" name="expiry-date">
//             <input type="time" name="expiry-time">
//             <textarea name="desc" placeholder="Description"></textarea>
//             `;
//             break;
//         case 'clothes':
//             formFieldsDiv.innerHTML = `
//                 <input type="text" name="gender" placeholder="Gender">
//                 <input type="text" name="size" placeholder="Clothing Size">
//                 <input type="text" name="cond" placeholder="Condition">
//                 <textarea name="desc" placeholder="Description"></textarea>
//             `;
//             break;
//         case 'groceries':
//             formFieldsDiv.innerHTML = `
//                 <input type="date" name="expiry-date">
//                 <input type="time" name="expiry-time">
//                 <textarea name="desc" placeholder="Description"></textarea>
//             `;
//             break;
//         case 'toys':
//             formFieldsDiv.innerHTML = `
//                 <input type="text" name="age-group" placeholder="Age Group">
//                 <input type="text" name="cond" placeholder="Condition">
//                 <textarea name="desc" placeholder="Description"></textarea>
//             `;
//             break;
//         case 'others':
//                 formFieldsDiv.innerHTML = `
//                     <textarea name="desc" placeholder="Description"></textarea>
//                 `;
//             break;
//         default:
//             // Do nothing
//             break;
//     }
// }

// // Event listener for category dropdown change
// document.getElementById('category').addEventListener('change', function() {
//     const selectedCategory = this.value;
//     generateFormFields(selectedCategory);
// });

// // JavaScript for handling form submission (to be implemented)
// document.getElementById('post-form').addEventListener('submit', function(event) {
//     event.preventDefault();
//     // Handle form submission (e.g., send data to server)
//     // This will be implemented in your Django backend
// });
