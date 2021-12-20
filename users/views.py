from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView

from users.models import User, Country
from .forms import CustomLoginForm, RegisterForm


class LoginViewList(LoginView):
    template_name = 'users/login.html'
    form_class = CustomLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('contact'))
        return super(LoginViewList, self).dispatch(request, *args, **kwargs)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        kwargs['country_data'] = Country.objects.all()
        return super().get_context_data(**kwargs)








