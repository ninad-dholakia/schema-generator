// scripts.js
function displayFileName() {
    const fileInput = document.getElementById('file_input');
    const selectedFilename = document.getElementById('selected_filename');
    selectedFilename.textContent = fileInput.files[0] ? fileInput.files[0].name : 'No file selected';
}