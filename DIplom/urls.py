"""
URL configuration for DIplom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from main import views as main_views
from userprofile import views as user_views
from cart import views as cart_views
from review import views as review_views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", main_views.IndexView.as_view(), name='home'),
    path('genre/<int:genre_id>/', main_views.ChooseGenre.as_view(), name='genre'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("registration/", user_views.RegistrationView.as_view(), name='registration'),
    path("profile/", user_views.ProfileView.as_view(), name='profile'),
    path('book/<int:pk>/', main_views.BookDetailView.as_view(), name='book_detail'),
    path('cart/', cart_views.CartView.as_view(), name='cart'),
    path('add-to-cart/<int:book_id>/', cart_views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', cart_views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('change-quantity/<int:item_id>/', cart_views.ChangeQuantityView.as_view(), name='change_quantity'),
    path('vectorize/', main_views.BookVectorView.as_view(), name='vectorize_book'),
    path('vector-display/', main_views.VectorDisplayView.as_view(), name='vector_display'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
