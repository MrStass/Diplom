document.querySelectorAll('.change-quantity-form').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {'X-CSRFToken': formData.get('csrfmiddlewaretoken')},
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const totalCell = this.closest('tr').querySelector('.total-price');
                totalCell.innerText = `${data.total_price} грн`; // оновлення загальної ціни товару
                document.querySelector('#cart-total').innerText = `${data.cart_total} грн`; // оновлення загальної суми кошика
            }
        })
        .catch(error => console.error('Error:', error));
    });
});