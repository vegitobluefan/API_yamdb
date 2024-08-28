from django.conf import settings
from django.contrib.auth import get_user_model  # Временная заглушка
from django.contrib.auth.models import AbstractUser
from django.db import models

user = get_user_model()  # Временная заглушка


# class User(AbstractUser):
#    """Кастомная модель пользователя."""


class NameSlugMixin(models.Model):
    """Миксин для полей name и slug."""

    name = models.CharField(
        max_length=settings.MAX_CHAR_LEN,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=settings.MAX_SLUG_LEN,
        verbose_name='Слаг',
    )

    class Meta:
        abstract = True


class Categories(NameSlugMixin):
    """Модель для категорий произведений."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class Genres(NameSlugMixin):
    """Модель для жанров произведений."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.title


class Titles(models.Model):
    """Модель для произведений."""

    name = models.CharField(
        max_length=settings.MAX_CHAR_LEN,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
    )
    description = models.CharField(
        verbose_name='Описание произведения',
        max_length=settings.MAX_CHAR_LEN,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        Categories,
        related_name='titles',
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.title
