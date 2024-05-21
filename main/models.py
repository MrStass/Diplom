from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre, related_name='books')
    author = models.ManyToManyField(Author, max_length=255)
    year = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='books/', null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    book_format = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, null=True)
    page_count = models.IntegerField(blank=True, null=True)
    cover_type = models.CharField(max_length=100, blank=True, null=True)
    book_type = models.CharField(max_length=100, null=True)
    original_name = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_available = models.BooleanField(default=True)

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / reviews.count()
        return 0

    def __str__(self):
        return self.title


class BookVector(models.Model):
    book = models.OneToOneField(Book, related_name='vector', on_delete=models.CASCADE)
    vector = models.BinaryField()

    def __str__(self):
        return f"Vector for {self.book.title}"


class RecommendedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recommendations', null=True)
    recommended = models.ManyToManyField(Book, related_name='recommendations_for', null=True)

    def __str__(self):
        return f'Recommendations for user {self.user.username}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.book.title} favorited by {self.user.username}"
