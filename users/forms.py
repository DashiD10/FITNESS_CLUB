from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    """Кастомная форма аутентификации с Bootstrap 5 стилями"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap 5 классы ко всем полям
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class UserRegistrationForm(UserCreationForm):
    """Кастомная форма регистрации с Bootstrap 5 стилями и валидацией email"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap 5 классы ко всем полям
        for field_name, field in self.fields.items():
            if field_name not in ['username', 'email', 'password1', 'password2']:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        """Проверяет уникальность email"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
