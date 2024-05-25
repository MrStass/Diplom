from django.db.models import Max
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Order, OrderItem
from main.models import Book
from cart.models import Cart, CartItem
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


class PurchaseView(LoginRequiredMixin, View):
    def get(self, request, book_id=None):
        cart = Cart.objects.get(user=request.user)
        books = []
        total_price = 0

        if book_id:
            # Якщо book_id передано, додається вибрана книга до списку книг
            book = get_object_or_404(Book, id=book_id)
            book_in_cart = False
            for item in cart.items.all():
                if item.book.id == book_id:
                    book_in_cart = True
                books.append((item.book, item.quantity))
                total_price += item.book.price * item.quantity
            if not book_in_cart:
                books.append((book, 1))
                total_price += book.price
        else:
            # Якщо book_id не передано, додаються всі книги з кошика
            cart_items = cart.items.all()
            for item in cart_items:
                books.append((item.book, item.quantity))
                total_price += item.book.price * item.quantity

        context = {
            'books': books,
            'total_price': total_price,
            'user': request.user
        }
        return render(request, 'purchase.html', context)

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        # Отримати максимальний order_number для цього користувача
        max_order_number = Order.objects.filter(user=request.user).aggregate(Max('order_number'))['order_number__max']
        if max_order_number is None:
            max_order_number = 0

        # Створення нового замовлення
        order = Order.objects.create(
            user=request.user,
            contact_email=request.POST.get('email'),
            contact_phone=request.POST.get('phone'),
            delivery_address=f"{request.POST.get('city')}, {request.POST.get('street')}, {request.POST.get('house')}, Кв/Офіс {request.POST.get('apartment')}",
            payment_method=request.POST.get('payment_method'),
            card_details=f"{request.POST.get('card_number')}, {request.POST.get('card_expiry')}, {request.POST.get('card_cvv')}" if request.POST.get(
                'payment_method') == 'card' else '',
            order_number=max_order_number + 1
        )

        # Додавання товарів з кошика до замовлення
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                unit_price=item.book.price
            )

        # Якщо book_id передано, додається вибрана книга до замовлення
        book_id = request.POST.get('book_id')
        if book_id:
            book = get_object_or_404(Book, id=book_id)
            if not cart.items.filter(book=book).exists():
                OrderItem.objects.create(
                    order=order,
                    book=book,
                    quantity=1,
                    unit_price=book.price
                )

        # Очищення кошика після оформлення замовлення
        cart.items.all().delete()

        return redirect('order_confirmation')

# Представлення для додавання книги до кошика та перенаправлення на сторінку покупки
class AddToCartAndPurchaseView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return redirect('purchase')

# Представлення для підтвердження замовлення
class OrderConfirmationView(TemplateView):
    template_name = 'order_confirmation.html'