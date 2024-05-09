from django.db import models
from django.contrib.auth.models import User
from main.models import Book


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username}: {self.rating}"