from main.models import *
from cart.models import *


def get_all_genres(request):
    return {
        'genres': Genre.objects.all()
    }


def cart_processor(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.books.count()
    else:
        cart_items_count = 0
    return {'cart_count': cart_items_count}