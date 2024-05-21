document.addEventListener('DOMContentLoaded', function() {
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
                        reviewDiv.querySelector('p:nth-child(2)').innerHTML = `
                            <strong>Рейтинг:</strong>
                            <span class="rating-display" data-rating="${data.review.rating}"></span>
                        `;
                        reviewDiv.querySelector('p:nth-child(3)').textContent = data.review.text;
                        updateRatingsDisplay();
                        document.getElementById('average-rating').innerHTML = `
                            <strong>Рейтинг:</strong>
                            <span class="rating-display" data-rating="${data.average_rating.toFixed(1)}"></span>
                        `;
                        updateRatingsDisplay();
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
                    document.getElementById('average-rating').innerHTML = `
                        <strong>Рейтинг:</strong>
                        <span class="rating-display" data-rating="${data.average_rating.toFixed(1)}"></span>
                    `;
                    updateRatingsDisplay();
                } else {
                    alert('Виникла помилка при видаленні відгуку.');
                }
            });
        });
    }

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
                    <p>
                        <strong>Рейтинг:</strong>
                        <span class="rating-display" data-rating="${data.review.rating}"></span>
                    </p>
                    <p>${data.review.text}</p>
                    <button class="btn btn-outline-primary edit-review-button" data-review-id="${data.review.id}">Редагувати</button>
                    <button class="btn btn-outline-danger delete-review-button" data-review-id="${data.review.id}">Видалити</button>
                    <div class="edit-review-form" id="edit-review-form-${data.review.id}" style="display: none;">
                        <form method="post" action="/review/update/${data.review.id}/">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${formData.get('csrfmiddlewaretoken')}">
                            <div class="review-form-group">
                                <label for="rating">Рейтинг:</label>
                                <div class="rating">
                                    <input type="radio" name="rating" id="edit-rating-5-${data.review.id}" value="5" ${data.review.rating == 5 ? 'checked' : ''}><label for="edit-rating-5-${data.review.id}">★</label>
                                    <input type="radio" name="rating" id="edit-rating-4-${data.review.id}" value="4" ${data.review.rating == 4 ? 'checked' : ''}><label for="edit-rating-4-${data.review.id}">★</label>
                                    <input type="radio" name="rating" id="edit-rating-3-${data.review.id}" value="3" ${data.review.rating == 3 ? 'checked' : ''}><label for="edit-rating-3-${data.review.id}">★</label>
                                    <input type="radio" name="rating" id="edit-rating-2-${data.review.id}" value="2" ${data.review.rating == 2 ? 'checked' : ''}><label for="edit-rating-2-${data.review.id}">★</label>
                                    <input type="radio" name="rating" id="edit-rating-1-${data.review.id}" value="1" ${data.review.rating == 1 ? 'checked' : ''}><label for="edit-rating-1-${data.review.id}">★</label>
                                </div>
                            </div>
                            <div class="review-form-group">
                                <label for="text">Відгук:</label>
                                <textarea name="text" id="text" class="review-textarea form-control">${data.review.text}</textarea>
                            </div>
                            <button type="submit" class="btn btn-primary">Оновити</button>
                        </form>
                    </div>
                `;
                reviewsDiv.appendChild(newReview);
                form.reset();
                document.getElementById('average-rating').innerHTML = `
                    <strong>Рейтинг:</strong>
                    <span class="rating-display" data-rating="${data.average_rating.toFixed(1)}"></span>
                `;
                updateRatingsDisplay();
                addEditEventListener(newReview.querySelector('.edit-review-button'));
                addDeleteEventListener(newReview.querySelector('.delete-review-button'));
            } else {
                alert('Виникла помилка при додаванні відгуку.');
            }
        });
    });

    document.querySelectorAll('.edit-review-button').forEach(button => {
        addEditEventListener(button);
    });

    document.querySelectorAll('.delete-review-button').forEach(button => {
        addDeleteEventListener(button);
    });

    function updateRatingsDisplay() {
        document.querySelectorAll('.rating-display').forEach(function(span) {
            const rating = parseFloat(span.getAttribute('data-rating'));
            const fullStars = Math.floor(rating);
            const halfStar = rating % 1 >= 0.5;
            span.innerHTML = '';

            for (let i = 1; i <= 5; i++) {
                if (i <= fullStars) {
                    span.innerHTML += '★';
                } else {
                    span.innerHTML += '☆';
                }
            }
        });
    }

    updateRatingsDisplay();

    document.querySelectorAll('.rating input').forEach(function(radio) {
        radio.addEventListener('change', function() {
            updateRatingStars(this);
        });
    });

    function updateRatingStars(radio) {
        const ratingDiv = radio.closest('.rating');
        const radios = ratingDiv.querySelectorAll('input');
        let matched = false;
        radios.forEach(r => {
            if (matched || r.checked) {
                r.nextElementSibling.classList.add('selected');
                matched = true;
            } else {
                r.nextElementSibling.classList.remove('selected');
            }
        });
    }

    document.querySelectorAll('.rating input:checked').forEach(function(radio) {
        updateRatingStars(radio);
    });

    document.querySelectorAll('#add-review-form .rating input').forEach(function(radio) {
        radio.addEventListener('change', function() {
            updateRatingStars(this);
        });
    });

    document.querySelectorAll('#add-review-form .rating input:checked').forEach(function(radio) {
        updateRatingStars(radio);
    });
});