from django import forms
from .models import Review

# Форма для відгуків
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        labels = {
            'text': 'Текст',
            'rating': 'Рейтинг (1-5)',
        }
        widgets = {
            # Віджет для поля тексту відгуку
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            # Віджет для поля рейтингу
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }