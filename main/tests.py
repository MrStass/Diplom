from django.test import TestCase
from django.urls import reverse
from main.models import Book, BookVector, Favorite, RecommendedBook
from cart.models import Cart, CartItem
from review.models import Review
from orders.models import Order, OrderItem
from django.contrib.auth.models import User
import pickle
import numpy as np
from django.core.files.uploadedfile import SimpleUploadedFile

# Тест для додавання відгуку
class AddReviewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.book = Book.objects.create(
            title='Test Book',
            price=100,
            year=2021,
            description='A test book description.'
        )
        vector = np.random.rand(10).astype(np.float32)
        self.book_vector = BookVector.objects.create(book=self.book, vector=pickle.dumps(vector))
        self.client.login(username='testuser', password='12345')

    def test_add_review(self):
        url = reverse('add_review', kwargs={'book_id': self.book.id})
        response = self.client.post(url, {
            'rating': 5,
            'text': 'Great book!'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.book, self.book)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.text, 'Great book!')

# Тест для оновлення відгуку
class UpdateReviewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.book = Book.objects.create(
            title='Test Book',
            price=100,
            year=2021,
            description='A test book description.'
        )
        vector = np.random.rand(10).astype(np.float32)
        self.book_vector = BookVector.objects.create(book=self.book, vector=pickle.dumps(vector))
        self.review = Review.objects.create(
            user=self.user,
            book=self.book,
            rating=5,
            text='Great book!'
        )
        self.client.login(username='testuser', password='12345')

    def test_update_review(self):
        url = reverse('update_review', kwargs={'review_id': self.review.id})
        response = self.client.post(url, {
            'rating': 4,
            'text': 'Good book!'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.text, 'Good book!')

# Тест для видалення відгуку
class DeleteReviewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.book = Book.objects.create(
            title='Test Book',
            price=100,
            year=2021,
            description='A test book description.'
        )
        vector = np.random.rand(10).astype(np.float32)
        self.book_vector = BookVector.objects.create(book=self.book, vector=pickle.dumps(vector))
        self.review = Review.objects.create(
            user=self.user,
            book=self.book,
            rating=5,
            text='Great book!'
        )
        self.client.login(username='testuser', password='12345')

    def test_delete_review(self):
        url = reverse('delete_review', kwargs={'review_id': self.review.id})
        response = self.client.post(url, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Review.objects.count(), 0)

# Тест для перемикання статусу улюбленої книги
class ToggleFavoriteTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.book = Book.objects.create(
            title='Test Book',
            price=100,
            year=2021,
            description='A test book description.'
        )
        vector = np.random.rand(10).astype(np.float32)
        self.book_vector = BookVector.objects.create(book=self.book, vector=pickle.dumps(vector))
        self.client.login(username='testuser', password='12345')

    def test_toggle_favorite(self):
        url = reverse('toggle_favorite', kwargs={'book_id': self.book.id})
        response = self.client.post(url, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorite.objects.filter(user=self.user, book=self.book).exists())
        response = self.client.post(url, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favorite.objects.filter(user=self.user, book=self.book).exists())

# Тест для перегляду детальної інформації про книгу
class BookDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.book = Book.objects.create(
            title='Test Book',
            price=100,
            year=2021,
            description='A test book description.',
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )
        vector = np.random.rand(10).astype(np.float32)
        self.book_vector = BookVector.objects.create(book=self.book, vector=pickle.dumps(vector))

    def test_book_detail_view(self):
        url = reverse('book_detail', kwargs={'pk': self.book.pk})
        self.client.login(username='testuser', password='12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

# Тест для перегляду нових надходжень
class NewArrivalsViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.book1 = Book.objects.create(title='Book 1', price=100, year=2021, description='Description 1', image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'))
        self.book2 = Book.objects.create(title='Book 2', price=150, year=2021, description='Description 2', image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'))
        self.book3 = Book.objects.create(title='Book 3', price=200, year=2021, description='Description 3', image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'))
        self.book4 = Book.objects.create(title='Book 4', price=250, year=2021, description='Description 4', image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'))
        self.book5 = Book.objects.create(title='Book 5', price=300, year=2021, description='Description 5', image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'))
        self.book6 = Book.objects.create(title='Book 6', price=350, year=2021, description='Description 6', image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'))
        vector1 = np.random.rand(10).astype(np.float32)
        self.book_vector1 = BookVector.objects.create(book=self.book1, vector=pickle.dumps(vector1))
        vector2 = np.random.rand(10).astype(np.float32)
        self.book_vector2 = BookVector.objects.create(book=self.book2, vector=pickle.dumps(vector2))
        vector3 = np.random.rand(10).astype(np.float32)
        self.book_vector3 = BookVector.objects.create(book=self.book3, vector=pickle.dumps(vector3))
        vector4 = np.random.rand(10).astype(np.float32)
        self.book_vector4 = BookVector.objects.create(book=self.book4, vector=pickle.dumps(vector4))
        vector5 = np.random.rand(10).astype(np.float32)
        self.book_vector5 = BookVector.objects.create(book=self.book5, vector=pickle.dumps(vector5))
        vector6 = np.random.rand(10).astype(np.float32)
        self.book_vector6 = BookVector.objects.create(book=self.book6, vector=pickle.dumps(vector6))

    def test_new_arrivals_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book6.title)
        self.assertContains(response, self.book5.title)
        self.assertContains(response, self.book4.title)
        self.assertContains(response, self.book3.title)
        self.assertContains(response, self.book2.title)

# Тест для перегляду улюблених книг
class FavoriteBooksViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.book = Book.objects.create(title='Test Book', price=100, year=2021, description='A test book description.')
        vector = np.random.rand(10).astype(np.float32)
        self.book_vector = BookVector.objects.create(book=self.book, vector=pickle.dumps(vector))
        Favorite.objects.create(user=self.user, book=self.book)
        self.client.login(username='testuser', password='12345')

    def test_favorite_books_view(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

# Тест для видалення улюблених книг за допомогою AJAX
class RemoveFavoriteAjaxTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.book = Book.objects.create(title='Test Book', price=100, year=2021, description='A test book description.')
        vector = np.random.rand(10).astype(np.float32)
        self.book_vector = BookVector.objects.create(book=self.book, vector=pickle.dumps(vector))
        Favorite.objects.create(user=self.user, book=self.book)
        self.client.login(username='testuser', password='12345')

    def test_remove_favorite_ajax(self):
        url = reverse('toggle_favorite', kwargs={'book_id': self.book.id})
        response = self.client.post(url, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favorite.objects.filter(user=self.user, book=self.book).exists())

# Тест для перегляду замовлень користувача
class ViewUserOrdersTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.order = Order.objects.create(user=self.user, delivery_address='Test Street', payment_method='cash', contact_phone='123456789')
        self.book = Book.objects.create(title='Test Book', price=100, year=2021, description='A test book description.')
        self.order_item = OrderItem.objects.create(order=self.order, book=self.book, quantity=1, unit_price=self.book.price)
        self.client.login(username='testuser', password='12345')

    def test_view_orders(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.id)
        self.assertContains(response, self.book.title)

# Тест для додавання рекомендації
class AddRecommendationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.book = Book.objects.create(
            title='Test Book',
            price=100,
            year=2021,
            description='A test book description.'
        )
        vector = np.random.rand(10).astype(np.float32)
        self.book_vector = BookVector.objects.create(book=self.book, vector=pickle.dumps(vector))
        self.client.login(username='testuser', password='12345')

    def test_add_recommendation(self):
        recommended_book = RecommendedBook.objects.create(user=self.user)
        recommended_book.recommended.add(self.book)
        self.assertEqual(RecommendedBook.objects.count(), 1)
        self.assertEqual(recommended_book.recommended.first(), self.book)
        self.assertEqual(recommended_book.user, self.user)