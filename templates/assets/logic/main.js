// script.js
document.addEventListener('DOMContentLoaded', function() {
    // JavaScript code to execute after the DOM has loaded
    console.log('DOM is ready');
    
    // Example: Changing text color on click
    let paragraph = document.querySelector('p');
    paragraph.addEventListener('click', function() {
        paragraph.style.color = 'red';
    });
});
