document.querySelectorAll('.edit-btn').forEach(button => {
    button.addEventListener('click', function () {
        const noteBlock = this.closest('.note-block');
        noteBlock.querySelector('.note-content').classList.add('d-none');
        noteBlock.querySelector('.edit-form').classList.remove('d-none');
        noteBlock.querySelector('.edit-controls').classList.add('d-none'); // ⬅ скрыть кнопки
    });
});

document.querySelectorAll('.cancel-btn').forEach(button => {
    button.addEventListener('click', function () {
        const noteBlock = this.closest('.note-block');
        noteBlock.querySelector('.edit-form').classList.add('d-none');
        noteBlock.querySelector('.note-content').classList.remove('d-none');
        noteBlock.querySelector('.edit-controls').classList.remove('d-none'); // ⬅ показать кнопки
    });
});
