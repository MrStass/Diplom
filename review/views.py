from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Review
from main.models import Book
from .forms import ReviewForm


# Представлення для додавання відгуку
@login_required  # Перевіряє, що користувач увійшов у систему
@require_POST  # Обмежує доступ тільки до POST-запитів
def add_review(request, book_id):
    # Отримання об'єкта книги або повернення 404, якщо книга не знайдена
    book = get_object_or_404(Book, id=book_id)
    # Ініціалізація форми відгуку з даними з POST-запиту
    form = ReviewForm(request.POST)
    if form.is_valid():
        # Збереження відгуку без коміта до бази даних
        review = form.save(commit=False)
        # Призначення користувача та книги до відгуку
        review.user = request.user
        review.book = book
        # Збереження відгуку у базі даних
        review.save()
        # Обчислення середнього рейтингу для книги
        average_rating = book.average_rating()
        # Повернення успішної відповіді з даними відгуку та середнім рейтингом
        return JsonResponse({
            'success': True,
            'review': {
                'id': review.id,
                'user': review.user.username,
                'text': review.text,
                'rating': review.rating,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
            },
            'average_rating': average_rating
        })
    # Повернення відповіді з помилками форми у випадку невалідності
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

# Представлення для видалення відгуку
@login_required  # Перевіряє, що користувач увійшов у систему
@require_POST  # Обмежує доступ тільки до POST-запитів
def delete_review(request, review_id):
    # Отримання об'єкта відгуку або повернення 404, якщо відгук не знайдено
    review = get_object_or_404(Review, id=review_id, user=request.user)
    # Збереження об'єкта книги перед видаленням відгуку
    book = review.book
    # Видалення відгуку
    review.delete()
    # Обчислення середнього рейтингу для книги
    average_rating = book.average_rating()
    # Повернення успішної відповіді з новим середнім рейтингом
    return JsonResponse({
        'success': True,
        'average_rating': average_rating
    })


# Представлення для оновлення відгуку
@login_required  # Перевіряє, що користувач увійшов у систему
@require_POST  # Обмежує доступ тільки до POST-запитів
def update_review(request, review_id):
    # Отримання об'єкта відгуку або повернення 404, якщо відгук не знайдено
    review = get_object_or_404(Review, id=review_id, user=request.user)
    # Ініціалізація форми відгуку з даними з POST-запиту та існуючого відгуку
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
        # Збереження оновленого відгуку у базі даних
        form.save()
        # Збереження об'єкта книги після оновлення відгуку
        book = review.book
        # Обчислення середнього рейтингу для книги
        average_rating = book.average_rating()
        # Повернення успішної відповіді з даними оновленого відгуку та середнім рейтингом
        return JsonResponse({
            'success': True,
            'review': {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'updated_at': review.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            },
            'average_rating': average_rating
        })
    # Повернення відповіді з помилками форми у випадку невалідності
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)