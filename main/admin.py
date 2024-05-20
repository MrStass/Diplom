from django.contrib import admin

from .models import Book, Genre, BookVector, Author, RecommendedBook, Favorite

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(BookVector)
admin.site.register(Author)
admin.site.register(RecommendedBook)
admin.site.register(Favorite)