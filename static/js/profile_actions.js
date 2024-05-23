// Функція для перемикання між відображенням поля та його редагуванням
function toggleEdit(field) {
    document.getElementById(`${field}-display`).classList.toggle('d-none'); // Перемикання видимості відображення поля
    document.getElementById(`${field}-form`).classList.toggle('d-none'); // Перемикання видимості форми редагування
}

// Функція для оновлення профілю користувача
function updateProfile(field) {
    const form = document.getElementById(`${field}-form`); // Отримання форми за ідентифікатором
    const formData = new FormData(form); // Створення об'єкта FormData з даних форми

    // Відправка запиту на сервер для оновлення профілю
    fetch('/profile/update/', {
        method: 'POST',
        body: new URLSearchParams(formData), // Перетворення FormData в URLSearchParams
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // Додавання CSRF-токену до заголовків
        }
    })
    .then(response => response.json()) // Перетворення відповіді в JSON
    .then(data => {
        if (data.success) {
            // Оновлення тексту відображення поля новим значенням
            document.getElementById(`${field}-display`).innerText = formData.get(field);
            toggleEdit(field); // Перемикання назад до режиму відображення
        } else {
            console.error(data.errors); // Виведення помилок в консоль
            alert('Error updating profile'); // Виведення повідомлення про помилку
        }
    })
    .catch(error => {
        console.error('Error:', error); // Виведення помилки в консоль
        alert('Error updating profile'); // Виведення повідомлення про помилку
    });
}