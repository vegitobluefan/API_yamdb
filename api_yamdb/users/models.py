from api_yamdb.settings import MAX_LEN_BIO, MAX_VALUE
from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

TEXT_CHOISES = [
    ('admin', ADMIN),
    ('moderator', MODERATOR),
    ('user', USER)
]


class User(AbstractUser):
    """Модель для описания пользователя."""
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True
    )
    bio = models.CharField(
        verbose_name='Биография',
        max_length=MAX_LEN_BIO,
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=TEXT_CHOISES,
        default=USER,
        max_length=MAX_VALUE
    )

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
