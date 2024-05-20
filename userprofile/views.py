from django.contrib.auth import login, authenticate
from django.views.generic import FormView, TemplateView
from main.models import Favorite
from orders.models import Order
from userprofile.forms import RegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin


class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        user = authenticate(self.request, username=user.username, password=form.cleaned_data['password'])
        login(request=self.request, user=user)
        return super(RegistrationView, self).form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['favorite_books'] = Favorite.objects.filter(user=self.request.user)

        orders = Order.objects.filter(user=self.request.user).prefetch_related('items__book')
        for order in orders:
            order.total_amount = sum(item.total_price() for item in order.items.all())

        context['orders'] = orders
        return context
