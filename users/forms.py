from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.contrib.auth.models import User
from .models import UserProfile


class UserLoginForm(AuthenticationForm):
    """Кастомная форма аутентификации с Bootstrap 5 стилями"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap 5 классы ко всем полям
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.get_placeholder(field_name)
            })

    def get_placeholder(self, field_name):
        placeholders = {
            'username': 'Введите имя пользователя',
            'password': 'Введите пароль'
        }
        return placeholders.get(field_name, '')


class UserRegisterForm(UserCreationForm):
    """Кастомная форма регистрации с Bootstrap 5 стилями и валидацией email"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap 5 классы ко всем полям
        for field_name, field in self.fields.items():
            if field_name not in ['username', 'email', 'password1', 'password2']:
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': self.get_placeholder(field_name)
                })
            # Убираем help_text для всех полей
            field.help_text = ''

    def get_placeholder(self, field_name):
        placeholders = {
            'username': 'Введите имя пользователя',
            'email': 'Введите email',
            'password1': 'Введите пароль',
            'password2': 'Повторите пароль'
        }
        return placeholders.get(field_name, '')

    def clean_email(self):
        """Проверяет уникальность email"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileUpdateForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap 5 классы ко всем полям
        for field_name, field in self.fields.items():
            if field_name == 'birth_date':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'type': 'date'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': self.get_placeholder(field_name)
                })

    def get_placeholder(self, field_name):
        placeholders = {
            'username': 'Введите имя пользователя',
            'email': 'Введите email',
            'telegram_id': 'Введите Telegram ID',
            'github_id': 'Введите GitHub ID'
        }
        return placeholders.get(field_name, '')

    class Meta:
        model = UserProfile
        fields = ('avatar', 'birth_date', 'telegram_id', 'github_id')


class UserPasswordChangeForm(PasswordChangeForm):
    """Форма для смены пароля"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap 5 классы ко всем полям
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.get_placeholder(field_name)
            })
            # Убираем help_text для всех полей
            field.help_text = ''

    def get_placeholder(self, field_name):
        placeholders = {
            'old_password': 'Введите текущий пароль',
            'new_password1': 'Введите новый пароль',
            'new_password2': 'Повторите новый пароль'
        }
        return placeholders.get(field_name, '')


class CustomPasswordResetForm(PasswordResetForm):
    """Кастомная форма для восстановления пароля"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap 5 классы к полю email
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите email для восстановления пароля'
        })


class CustomSetPasswordForm(SetPasswordForm):
    """Кастомная форма для установки нового пароля"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap 5 классы ко всем полям
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.get_placeholder(field_name)
            })
            # Убираем help_text для всех полей
            field.help_text = ''

    def get_placeholder(self, field_name):
        placeholders = {
            'new_password1': 'Введите новый пароль',
            'new_password2': 'Повторите новый пароль'
        }
        return placeholders.get(field_name, '')
