document.addEventListener('DOMContentLoaded', function() {
    // Функція обробки додавання товару до кошика
    function handleAddToCart(event) {
        event.preventDefault();
        const formData = new FormData(this);  // Отримання даних форми
        const bookId = this.getAttribute('data-book-id');  // Отримання ID книги з атрибуту форми
        const button = document.querySelector(`.add-to-cart-btn[data-book-id="${bookId}"]`);  // Кнопка додавання до кошика

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Оновлення стану кнопки додавання до кошика
                if (button) {
                    button.textContent = 'У кошику';
                    button.classList.remove('btn-primary');
                    button.classList.add('btn-success');
                    button.disabled = true;
                }

                // Оновлення рекомендацій
                fetch(window.location.href, {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newRecommendations = doc.querySelector('.recommended-books-container');  // Нові рекомендації
                    const oldRecommendations = document.querySelector('.recommended-books-container');  // Стара рекомендація
                    oldRecommendations.innerHTML = newRecommendations.innerHTML;  // Замінити старі рекомендації новими

                    loadAddToCartForms();  // Завантажити форми додавання до кошика
                    loadFavoriteButtons();  // Завантажити кнопки улюбленого
                })
                .catch(error => console.error('Error:', error));
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Функція завантаження форм додавання до кошика
    function loadAddToCartForms() {
        const addToCartForms = document.querySelectorAll('.add-to-cart-form');
        addToCartForms.forEach(form => {
            form.removeEventListener('submit', handleAddToCart);
            form.addEventListener('submit', handleAddToCart);
        });
    }

    // Ініціалізація завантаження форм додавання до кошика
    loadAddToCartForms();
    // Ініціалізація завантаження кнопок улюбленого
    loadFavoriteButtons();
});