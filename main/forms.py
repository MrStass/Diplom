from django import forms
from .models import Book


class BookVectorForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), label="Select a Book")
    description = forms.CharField(widget=forms.Textarea, label="Book Description")


class BookSelectForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), label="Виберіть книгу")