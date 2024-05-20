document.addEventListener('DOMContentLoaded', function() {
    // Обробка додавання відгуків
    document.getElementById('add-review-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const reviewsDiv = document.getElementById('reviews');
                const newReview = document.createElement('div');
                newReview.classList.add('review');
                newReview.setAttribute('id', `review-${data.review.id}`);
                newReview.innerHTML = `
                    <p><strong>${data.review.user}</strong> - ${data.review.created_at}</p>
                    <p>Рейтинг: ${data.review.rating}</p>
                    <p>${data.review.text}</p>
                    <button class="edit-review-button" data-review-id="${data.review.id}">Редагувати</button>
                    <button class="delete-review-button" data-review-id="${data.review.id}">Видалити</button>
                    <div class="edit-review-form" id="edit-review-form-${data.review.id}" style="display: none;">
                        <form method="post" action="/review/update/${data.review.id}/">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${formData.get('csrfmiddlewaretoken')}">
                            <div class="form-group">
                                <label for="id_text">Текст:</label>
                                <textarea name="text" class="form-control" rows="4">${data.review.text}</textarea>
                            </div>
                            <div class="form-group">
                                <label for="id_rating">Рейтинг:</label>
                                <input type="number" name="rating" class="form-control" value="${data.review.rating}" min="1" max="5">
                            </div>
                            <button type="submit" class="btn btn-primary">Оновити</button>
                        </form>
                    </div>
                `;
                reviewsDiv.appendChild(newReview);
                form.reset();
                // Оновлення середнього рейтингу
                document.getElementById('average-rating').textContent = `Рейтинг: ${data.average_rating.toFixed(1)} / 5`;
                // Додаємо обробники подій для нових кнопок редагування та видалення
                addEditEventListener(newReview.querySelector('.edit-review-button'));
                addDeleteEventListener(newReview.querySelector('.delete-review-button'));
            } else {
                alert('Виникла помилка при додаванні відгуку.');
            }
        });
    });

    function addEditEventListener(button) {
        button.addEventListener('click', function() {
            const reviewId = this.getAttribute('data-review-id');
            const editForm = document.getElementById(`edit-review-form-${reviewId}`);
            editForm.style.display = editForm.style.display === 'none' ? 'block' : 'none';
            editForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const form = e.target;
                const formData = new FormData(form);
                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const reviewDiv = document.getElementById(`review-${data.review.id}`);
                        reviewDiv.querySelector('p:nth-child(2)').textContent = `Рейтинг: ${data.review.rating}`;
                        reviewDiv.querySelector('p:nth-child(3)').textContent = data.review.text;
                        // Оновлення середнього рейтингу
                        document.getElementById('average-rating').textContent = `Рейтинг: ${data.average_rating.toFixed(1)} / 5`;
                        editForm.style.display = 'none';
                    } else {
                        alert('Виникла помилка при оновленні відгуку.');
                    }
                });
            });
        });
    }

    function addDeleteEventListener(button) {
        button.addEventListener('click', function() {
            const reviewId = this.getAttribute('data-review-id');
            const deleteUrl = `/review/delete/${reviewId}/`;
            fetch(deleteUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById(`review-${reviewId}`).remove();
                    // Оновлення середнього рейтингу
                    document.getElementById('average-rating').textContent = `Рейтинг: ${data.average_rating.toFixed(1)} / 5`;
                } else {
                    alert('Виникла помилка при видаленні відгуку.');
                }
            });
        });
    }

    document.querySelectorAll('.edit-review-button').forEach(button => {
        addEditEventListener(button);
    });

    document.querySelectorAll('.delete-review-button').forEach(button => {
        addDeleteEventListener(button);
    });
});