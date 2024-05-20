document.addEventListener("DOMContentLoaded", function() {
    function loadFavoriteButtons() {
        document.querySelectorAll('.book-favorite-btn').forEach(button => {
            button.removeEventListener('click', handleToggleFavorite);
            button.addEventListener('click', handleToggleFavorite);
        });
    }

    function handleToggleFavorite(event) {
        event.preventDefault();
        const button = this;
        const bookId = button.dataset.bookId;

        fetch(`/toggle-favorite/${bookId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                updateFavoriteButtons(bookId, data.action);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Помилка при виконанні запиту. Спробуйте ще раз.');
        });
    }

    function updateFavoriteButtons(bookId, action) {
        const buttons = document.querySelectorAll(`.book-favorite-btn[data-book-id="${bookId}"]`);
        buttons.forEach(button => {
            const icon = button.querySelector('i');
            if (action === 'add') {
                icon.classList.remove('far');
                icon.classList.add('fas');
                button.classList.add('favorite');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                button.classList.remove('favorite');
            }
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    loadFavoriteButtons();
    window.loadFavoriteButtons = loadFavoriteButtons; // Додано для доступу з іншого скрипта
});