from main.models import *
from cart.models import *


# Функція для отримання всіх жанрів та авторів
def get_all_genres_and_authors(request):
    return {
        'genres': Genre.objects.all(),
        'authors': Author.objects.all()
    }

# Процесор контексту для кошика
def cart_processor(request):
    if request.user.is_authenticated:
        # Отримати або створити кошик для користувача
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Підрахувати кількість елементів у кошику
        cart_items_count = cart.items.count()
    else:
        cart_items_count = 0
    return {'cart_count': cart_items_count}





