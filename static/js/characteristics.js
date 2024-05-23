// Додавання обробника події для кнопки "Показати всі деталі"
document.getElementById('view-all-details').addEventListener('click', function() {
    var details = document.getElementById('all-details');  // Елемент з усіма деталями
    var viewButtonContainer = document.getElementById('view-all-details-container');  // Контейнер з кнопкою "Показати всі деталі"
    var hideButtonContainer = document.getElementById('hide-details-container');  // Контейнер з кнопкою "Сховати деталі"

    details.style.display = 'block';  // Відображення всіх деталей
    viewButtonContainer.style.display = 'none';  // Сховати кнопку "Показати всі деталі"
    hideButtonContainer.style.display = 'block';  // Відображення кнопки "Сховати деталі"
});

// Додавання обробника події для кнопки "Сховати всі деталі"
document.getElementById('hide-all-details').addEventListener('click', function() {
    var details = document.getElementById('all-details');  // Елемент з усіма деталями
    var viewButtonContainer = document.getElementById('view-all-details-container');  // Контейнер з кнопкою "Показати всі деталі"
    var hideButtonContainer = document.getElementById('hide-details-container');  // Контейнер з кнопкою "Сховати деталі"

    details.style.display = 'none';  // Сховати всі деталі
    viewButtonContainer.style.display = 'block';  // Відображення кнопки "Показати всі деталі"
    hideButtonContainer.style.display = 'none';  // Сховати кнопку "Сховати деталі"
});