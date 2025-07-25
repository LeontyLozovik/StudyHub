document.querySelectorAll('.add-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        const courseList = this.closest('.card-body').querySelector('.course-list');
        courseList.classList.toggle('d-none');
    });
});
