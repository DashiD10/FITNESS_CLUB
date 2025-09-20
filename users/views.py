from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from .forms import (
    UserLoginForm, UserRegisterForm, UserProfileUpdateForm,
    UserPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
)
from .models import UserProfile


class UserRegisterView(CreateView):
    """Представление для регистрации пользователей"""
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('landing')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Автоматический вход после регистрации
        login(self.request, self.object)
        messages.success(self.request, 'Регистрация прошла успешно!')
        return response

    def dispatch(self, request, *args, **kwargs):
        # Защита от доступа аутентифицированных пользователей
        if request.user.is_authenticated:
            return redirect('landing')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class UserLoginView(LoginView):
    """Представление для входа пользователей"""
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Добро пожаловать!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход в систему'
        return context


class UserLogoutView(LogoutView):
    """Представление для выхода пользователей"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'Вы успешно вышли из системы!')
        return super().dispatch(request, *args, **kwargs)


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    """Представление для отображения профиля пользователя"""
    model = UserProfile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        # Получаем профиль текущего пользователя
        return get_object_or_404(UserProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мой профиль'
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования профиля пользователя"""
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = 'users/profile_update_form.html'
    success_url = reverse_lazy('users:profile_detail')

    def get_object(self):
        # Получаем профиль текущего пользователя
        return get_object_or_404(UserProfile, user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Профиль успешно обновлен!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Представление для смены пароля"""
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:profile_detail')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Пароль успешно изменен!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Смена пароля'
        return context


class CustomPasswordResetView(PasswordResetView):
    """Представление для восстановления пароля"""
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Письмо с инструкциями отправлено на ваш email!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Восстановление пароля'
        return context


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Представление для подтверждения отправки email"""
    template_name = 'users/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо отправлено'
        return context


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Представление для установки нового пароля"""
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Пароль успешно изменен!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установка нового пароля'
        return context


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Представление для подтверждения успешного сброса пароля"""
    template_name = 'users/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пароль изменен'
        return context
