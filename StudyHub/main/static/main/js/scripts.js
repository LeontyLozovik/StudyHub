document.addEventListener('DOMContentLoaded', function () {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('id_cover');

    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('bg-light');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('bg-light');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('bg-light');
        const files = e.dataTransfer.files;
        fileInput.files = files;
    });
});
