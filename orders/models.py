from django.db import models
from django.contrib.auth.models import User
from main.models import Book


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наложений платіж'),
        ('card', 'Картка'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    contact_email = models.EmailField(max_length=255, null=True)
    contact_phone = models.CharField(max_length=20, null=True)
    delivery_address = models.CharField(max_length=255, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True)
    card_details = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"
