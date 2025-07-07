document.addEventListener('DOMContentLoaded', function () {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('id_avatar');
    const textDisplay = document.getElementById('drop-zone-text');

    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            textDisplay.textContent = `Выбран файл: ${files[0].name}`;
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            textDisplay.textContent = `Выбран файл: ${fileInput.files[0].name}`;
        }
    });
});