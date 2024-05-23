// Знаходження всіх форм зміни кількості товару та додавання обробника подій для кожної форми
document.querySelectorAll('.change-quantity-form').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Запобігання стандартної відправки форми

        const formData = new FormData(this);  // Отримання даних форми

        // Виконання запиту через fetch
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')  // Додавання CSRF-токену до заголовків
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())  // Перетворення відповіді в JSON
        .then(data => {
            if (data.status === 'success') {
                // Оновлення загальної ціни товару у відповідній комірці таблиці
                const totalCell = this.closest('tr').querySelector('.total-price');
                totalCell.innerText = `${data.total_price} грн`;  // Оновлення загальної ціни товару

                // Оновлення загальної суми кошика
                document.querySelector('#cart-total').innerText = `${data.cart_total} грн`;  // Оновлення загальної суми кошика
            }
        })
        .catch(error => console.error('Error:', error));  // Виведення помилки у консоль
    });
});