from django.dispatch import receiver
from .models import CartItem
from main.models import BookVector, RecommendedBook, Book
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=CartItem)
def update_recommendations_on_save(sender, instance, created, **kwargs):
    update_recommendations(instance.cart)


@receiver(post_delete, sender=CartItem)
def update_recommendations_on_delete(sender, instance, **kwargs):
    update_recommendations(instance.cart)


def update_recommendations(cart):
    cart_items = CartItem.objects.filter(cart=cart)
    user = cart.user

    if not cart_items.exists():
        RecommendedBook.objects.filter(user=user).delete()
        return

    book_ids_in_cart = [item.book.id for item in cart_items]
    cart_vectors = [pickle.loads(BookVector.objects.get(book_id=book_id).vector) for book_id in book_ids_in_cart]
    cart_matrix = np.vstack(cart_vectors)
    all_books = Book.objects.exclude(id__in=book_ids_in_cart)
    all_vectors = [pickle.loads(BookVector.objects.get(book=book).vector) for book in all_books]
    all_matrix = np.vstack(all_vectors)
    cosine_sim = cosine_similarity(cart_matrix, all_matrix)
    avg_similarity = np.mean(cosine_sim, axis=0)
    top_indices = np.argsort(avg_similarity)[::-1][:10]
    recommended_books = [all_books[int(i)] for i in top_indices]

    recommendation, created = RecommendedBook.objects.get_or_create(user=user)
    recommendation.recommended.set(recommended_books)
    recommendation.save()
