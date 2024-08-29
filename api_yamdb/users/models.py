from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_VARIANTS = [
    ('anon', 'anonimous'),
    ('admin', 'admin'),
    ('moderator', 'moderator'),
    ('user', 'user')
]


class User(AbstractUser):
    """Модель для описания пользователя."""
    email = models.EmailField(
        verbose_name="Электронная почта",
        unique=True
    )

    biography = models.CharField(
        verbose_name="Биография",
        max_length=100,
        blank=True,
        null=True
    )

    role = models.CharField(
        verbose_name='Роль',
        choices=ROLE_VARIANTS,
        default='user',
        max_length=10
    )

    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=200,
        editable=False,
        null=True,
        blank=True,
        unique=True
    )
