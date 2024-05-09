from django.contrib.auth import login, authenticate
from django.views.generic import FormView, TemplateView
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