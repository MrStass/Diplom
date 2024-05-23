from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


# Форма реєстрації користувачів
class RegistrationForm(forms.ModelForm):
    # Поля для паролю та підтвердження паролю
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    # Перевірка підтвердження паролю
    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return password_confirm

    # Збереження користувача з зашифрованим паролем
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

# Форма профілю користувача
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я користувача"}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email адреса'}),
        }

    # Перевірка валідності імені користувача
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[\w.@+-]{1,150}$', username):
            raise ValidationError('Користувач може містити лише букви, цифри та @/./+/-/_. і бути довжиною до 150 символів.')
        return username

    # Перевірка валідності електронної пошти
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,6}$', email):
            raise ValidationError('Введіть правильну адресу електронної пошти.')
        return email