from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Модель профиля пользователя"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )
    telegram_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Telegram ID'
    )
    github_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='GitHub ID'
    )

    objects = models.Manager()

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'Профиль {self.user.username}'
