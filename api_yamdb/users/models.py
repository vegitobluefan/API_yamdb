from django.db import models
from django.contrib.auth.models import AbstractUser
from api_yamdb.settings import (MAX_LEN_CODE, MAX_LEN_BIO, MAX_LEN_ROLE)

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
        # max_length=254,
        unique=True
    )

    bio = models.CharField(
        verbose_name="Биография",
        max_length=MAX_LEN_BIO,
        blank=True,
        null=True
    )

    role = models.CharField(
        verbose_name='Роль',
        choices=ROLE_VARIANTS,
        default='user',
        max_length=MAX_LEN_ROLE
    )

    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=MAX_LEN_CODE,
        editable=False,
        null=True,
        blank=True,
        unique=True
    )
