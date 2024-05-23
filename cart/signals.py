from django.dispatch import receiver
from .models import CartItem
from main.models import BookVector, RecommendedBook, Book
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
from django.db.models.signals import post_save, post_delete


# Обробник сигналу для оновлення рекомендацій при збереженні CartItem
@receiver(post_save, sender=CartItem)
def update_recommendations_on_save(sender, instance, created, **kwargs):
    update_recommendations(instance.cart)

# Обробник сигналу для оновлення рекомендацій при видаленні CartItem
@receiver(post_delete, sender=CartItem)
def update_recommendations_on_delete(sender, instance, **kwargs):
    update_recommendations(instance.cart)

# Функція для оновлення рекомендацій для користувача
def update_recommendations(cart):
    cart_items = CartItem.objects.filter(cart=cart)
    user = cart.user

    # Якщо кошик порожній, видалити всі рекомендації для користувача
    if not cart_items.exists():
        RecommendedBook.objects.filter(user=user).delete()
        return

    # Отримати ID книг у кошику
    book_ids_in_cart = [item.book.id for item in cart_items]
    # Отримати векторні представлення книг у кошику
    cart_vectors = [pickle.loads(BookVector.objects.get(book_id=book_id).vector) for book_id in book_ids_in_cart]
    cart_matrix = np.vstack(cart_vectors)
    # Отримати всі книги, які не знаходяться в кошику
    all_books = Book.objects.exclude(id__in=book_ids_in_cart)
    # Отримати векторні представлення всіх книг
    all_vectors = [pickle.loads(BookVector.objects.get(book=book).vector) for book in all_books]
    all_matrix = np.vstack(all_vectors)
    # Обчислити косинусну схожість між книгами у кошику та всіма іншими книгами
    cosine_sim = cosine_similarity(cart_matrix, all_matrix)
    avg_similarity = np.mean(cosine_sim, axis=0)
    # Отримати індекси книг з найбільшою схожістю
    top_indices = np.argsort(avg_similarity)[::-1][:10]
    recommended_books = [all_books[int(i)] for i in top_indices]

    # Оновити або створити рекомендації для користувача
    recommendation, created = RecommendedBook.objects.get_or_create(user=user)
    recommendation.recommended.set(recommended_books)
    recommendation.save()