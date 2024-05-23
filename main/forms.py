from django import forms
from .models import Book


# Форма для вибору книги та введення опису книги
class BookVectorForm(forms.Form):
    # Поле для вибору книги
    book = forms.ModelChoiceField(queryset=Book.objects.all(), label="Select a Book")
    # Поле для введення опису книги
    description = forms.CharField(widget=forms.Textarea, label="Book Description")

# Форма для вибору книги
class BookSelectForm(forms.Form):
    # Поле для вибору книги
    book = forms.ModelChoiceField(queryset=Book.objects.all(), label="Виберіть книгу")

# Форма для пошуку
class SearchForm(forms.Form):
    # Поле для введення пошукового запиту
    query = forms.CharField(label='Search', max_length=100)