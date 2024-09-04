from api_yamdb.settings import MAX_LEN_BIO, MAX_VALUE, MAX_EMAIL_LEN
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель для описания пользователя."""
    class Roles(models.TextChoices):
        """Класс ролей."""
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=MAX_EMAIL_LEN
    )
    bio = models.CharField(
        verbose_name='Биография',
        max_length=MAX_LEN_BIO,
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=Roles.choices,
        default=Roles.USER,
        max_length=MAX_VALUE
    )


    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.Roles.MODERATOR

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
