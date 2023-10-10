document.getElementById('uploadForm').addEventListener('submit', (event) => {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const fileName = file.name;
        if (!fileName.endsWith('.fasta')) {
            console.error('Invalid file type. Please select a .fasta file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('File uploaded successfully:', data);
        })
        .catch(error => {
            console.error('Error uploading file:', error);
        });
    } else {
        console.error('No file selected.');
    }
});
