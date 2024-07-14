document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Image uploaded successfully!');
    // Here, you can add the logic to send the image to the server for analysis
});

document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData();
    const fileField = document.getElementById('image-upload');

    formData.append('image', fileField.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        // Display colors
        displayColors(data.colors);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function displayColors(colors) {
    const resultsSection = document.createElement('section');
    resultsSection.classList.add('results');
    const resultsTitle = document.createElement('h2');
    resultsTitle.textContent = 'Analyzed Colors';
    resultsSection.appendChild(resultsTitle);

    colors.forEach(color => {
        const colorDiv = document.createElement('div');
        colorDiv.style.backgroundColor = color;
        colorDiv.classList.add('color-box');
        colorDiv.textContent = color;
        resultsSection.appendChild(colorDiv);
    });

    document.body.appendChild(resultsSection);
}

// scripts.js

document.addEventListener("DOMContentLoaded", function() {
    const contactForm = document.getElementById('contact-form');

    contactForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Get form values
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const subject = document.getElementById('subject').value.trim();
        const message = document.getElementById('message').value.trim();

        // Simple validation
        if (!name || !email || !subject || !message) {
            alert("Please fill in all fields.");
            return;
        }

        if (!validateEmail(email)) {
            alert("Please enter a valid email address.");
            return;
        }

        // Simulate sending data (here you would typically use an AJAX request)
        console.log("Form submitted with the following data:");
        console.log("Name: " + name);
        console.log("Email: " + email);
        console.log("Subject: " + subject);
        console.log("Message: " + message);

        // Clear the form
        contactForm.reset();

        // Display a success message
        alert("Your message has been sent successfully!");
    });

    function validateEmail(email) {
        // Basic email validation
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }
});