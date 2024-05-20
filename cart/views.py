from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Cart, CartItem, Book
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from main.models import RecommendedBook, Favorite
from django.http import JsonResponse


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return render(request, 'cart.html', {'cart': cart})


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        if not book.is_available:
            return JsonResponse({
                'status': 'error',
                'message': 'Книга недоступна для додавання до кошика'
            })

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Книга додана до кошика'
        })

class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = CartItem.objects.get(id=item_id)
        item.delete()
        return redirect(request.POST.get('next', '/cart/'))


class ChangeQuantityView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = CartItem.objects.get(id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        item.quantity = quantity
        item.save()
        cart = item.cart
        total_cart_price = sum(item.total_price() for item in cart.items.all())
        return JsonResponse({
            'status': 'success',
            'total_price': item.total_price(),
            'cart_total': total_cart_price
        })

