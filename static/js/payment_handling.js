document.addEventListener('DOMContentLoaded', function () {
    // Отримання елемента вибору способу оплати та контейнера з деталями картки
    const paymentSelect = document.getElementById('payment_method');
    const cardDetails = document.querySelector('.card-details');

    // Додавання обробника подій для зміни вибору способу оплати
    paymentSelect.addEventListener('change', function () {
        // Якщо вибрано оплату карткою, показати деталі картки
        if (this.value === 'card') {
            cardDetails.classList.remove('d-none');
        } else {
            // В іншому випадку сховати деталі картки
            cardDetails.classList.add('d-none');
        }
    });
});