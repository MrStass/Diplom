from django.shortcuts import render, redirect
from django.views import View
from .models import Cart, CartItem, Book
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from main.models import RecommendedBook

class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return render(request, 'cart.html', {'cart': cart})


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        book = Book.objects.get(id=book_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect(request.POST.get('next', '/'))


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = CartItem.objects.get(id=item_id)
        item.delete()
        return redirect(request.POST.get('next', '/cart/'))


class ChangeQuantityView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = CartItem.objects.get(id=item_id)
        quantity = request.POST.get('quantity', 1)
        item.quantity = int(quantity)
        item.save()
        return redirect('/cart/')

