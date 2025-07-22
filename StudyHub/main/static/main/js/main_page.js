document.addEventListener('DOMContentLoaded', function () {
  const buttons = document.querySelectorAll('.favorite-btn');

  const getCSRFToken = () => {
    const cookie = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
  };

  buttons.forEach(button => {
    button.addEventListener('click', function () {
      const icon = this.querySelector('.favorite-icon');
      const courseId = this.dataset.courseId;

      fetch(`/toggle_favorite/${courseId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({})
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'added') {
            icon.classList.remove('fa-regular');
            icon.classList.add('fa-solid', 'text-warning');
          } else {
            icon.classList.remove('fa-solid', 'text-warning');
            icon.classList.add('fa-regular');
          }
        })
        .catch(error => console.error('Error:', error));
    });
  });
});
