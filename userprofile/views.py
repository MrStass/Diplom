from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from main.models import Favorite
from orders.models import Order
from userprofile.forms import RegistrationForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Представлення для реєстрації користувачів
class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/'

    # Обробка успішної форми реєстрації
    def form_valid(self, form):
        # Збереження нового користувача
        user = form.save()
        # Аутентифікація користувача після реєстрації
        user = authenticate(self.request, username=user.username, password=form.cleaned_data['password'])
        # Вхід користувача у систему
        login(request=self.request, user=user)
        return super(RegistrationView, self).form_valid(form)

# Представлення для профілю користувача
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    # Отримання даних для контексту шаблону
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['favorite_books'] = Favorite.objects.filter(user=self.request.user)

        # Отримання останнього замовлення користувача для відображення номера телефону
        last_order = Order.objects.filter(user=self.request.user).order_by('-created_at').first()
        if last_order:
            context['phone_number'] = last_order.contact_phone
        else:
            context['phone_number'] = None

        # Додавання форми профілю користувача у контекст
        context['form'] = UserProfileForm(instance=self.request.user)
        # Отримання всіх замовлень користувача разом з пов'язаними книгами
        orders = Order.objects.filter(user=self.request.user).prefetch_related('items__book')
        for order in orders:
            # Обчислення загальної суми замовлення
            order.total_amount = sum(item.total_price() for item in order.items.all())

        context['orders'] = orders
        return context

    # Обробка POST-запиту для оновлення профілю користувача
    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)