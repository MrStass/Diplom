document.addEventListener('DOMContentLoaded', function() {
    // Функція обробки додавання товару до кошика
    function handleAddToCart(event) {
        event.preventDefault();
        const formData = new FormData(this);
        const bookId = this.getAttribute('data-book-id');
        const button = document.querySelector(`.add-to-cart-btn[data-book-id="${bookId}"]`);

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
                if (button) {
                    button.textContent = 'У кошику';
                    button.classList.remove('btn-primary');
                    button.classList.add('btn-success');
                    button.disabled = true;
                }

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
                    const newRecommendations = doc.querySelector('.recommended-books-container');
                    const oldRecommendations = document.querySelector('.recommended-books-container');
                    oldRecommendations.innerHTML = newRecommendations.innerHTML;

                    loadAddToCartForms();
                    loadFavoriteButtons();
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