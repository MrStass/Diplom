document.addEventListener("DOMContentLoaded", function() {
    // Функція для завантаження всіх кнопок улюблених книг
    function loadFavoriteButtons() {
        document.querySelectorAll('.book-favorite-btn').forEach(button => {
            button.removeEventListener('click', handleToggleFavorite); // Видалення існуючих обробників подій
            button.addEventListener('click', handleToggleFavorite); // Додавання нового обробника подій
        });
    }

    // Функція для обробки натискання на кнопку улюблених книг
    function handleToggleFavorite(event) {
        event.preventDefault();
        const button = this;
        const bookId = button.dataset.bookId; // Отримання ID книги з атрибуту кнопки

        fetch(`/toggle-favorite/${bookId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Додавання CSRF-токену до заголовків
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
                updateFavoriteButtons(bookId, data.action); // Оновлення стану кнопок улюблених книг
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Помилка при виконанні запиту. Спробуйте ще раз.');
        });
    }

    // Функція для оновлення стану кнопок улюблених книг
    function updateFavoriteButtons(bookId, action) {
        const buttons = document.querySelectorAll(`.book-favorite-btn[data-book-id="${bookId}"]`);
        buttons.forEach(button => {
            const icon = button.querySelector('i');
            if (action === 'add') {
                icon.classList.remove('far'); // Зміна іконки на заповнену
                icon.classList.add('fas');
                button.classList.add('favorite'); // Додавання класу "favorite" до кнопки
            } else {
                icon.classList.remove('fas'); // Зміна іконки на порожню
                icon.classList.add('far');
                button.classList.remove('favorite'); // Видалення класу "favorite" з кнопки
            }
        });
    }

    // Функція для отримання значення кукі за ім'ям
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

    // Завантаження всіх кнопок улюблених книг при завантаженні сторінки
    loadFavoriteButtons();
    window.loadFavoriteButtons = loadFavoriteButtons; // Додавання функції до глобального об'єкту
});