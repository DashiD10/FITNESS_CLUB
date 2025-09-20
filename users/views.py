from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserLoginForm, UserRegistrationForm


class UserLoginView(LoginView):
    """Представление для входа пользователей"""
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход в систему'
        context['button_text'] = 'Войти'
        return context


class UserRegistrationView(CreateView):
    """Представление для регистрации пользователей"""
    form_class = UserRegistrationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('landing')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['button_text'] = 'Зарегистрироваться'
        return context


class UserLogoutView(LogoutView):
    """Представление для выхода пользователей"""
    pass
