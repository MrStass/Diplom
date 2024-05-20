document.addEventListener('DOMContentLoaded', function () {
    const paymentSelect = document.getElementById('payment_method');
    const cardDetails = document.querySelector('.card-details');

    paymentSelect.addEventListener('change', function () {
        if (this.value === 'card') {
            cardDetails.classList.remove('d-none');
        } else {
            cardDetails.classList.add('d-none');
        }
    });
});