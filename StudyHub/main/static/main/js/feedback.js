const stars = document.querySelectorAll('.star');
const ratingInput = document.getElementById('id_rate');
let currentRating = 0;

stars.forEach((star, idx) => {
    const val = idx + 1;

    star.addEventListener('mouseenter', () => {
        highlightStars(val);
    });

    star.addEventListener('mouseleave', () => {
        highlightStars(currentRating);
    });

    star.addEventListener('click', () => {
        currentRating = val;
        ratingInput.value = val;
        highlightStars(val);
    });
});

function highlightStars(rating) {
    stars.forEach((star, idx) => {
        if (idx < rating) {
            star.classList.add('fa-solid');
            star.classList.remove('fa-regular');
            star.style.color = '#f5c518';
        } else {
            star.classList.add('fa-regular');
            star.classList.remove('fa-solid');
            star.style.color = '#ccc';
        }
    });
}