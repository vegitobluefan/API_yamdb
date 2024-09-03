from api_yamdb.settings import MAX_LEN_BIO, MAX_LEN_CODE, MAX_VALUE
from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_VARIANTS = [
    ('admin', 'admin'),
    ('moderator', 'moderator'),
    ('user', 'user')
]

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


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
        choices=ROLE_VARIANTS,
        default='user',
        max_length=MAX_VALUE
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=MAX_LEN_CODE,
        editable=False,
        null=True,
        blank=True,
        unique=True
    )

    @property
    def is_admin(self):
        return any(
            [self.role == 'admin', self.is_superuser, self.is_staff]
        )

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == USER
