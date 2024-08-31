from django.conf import settings
from django.contrib.auth import get_user_model  # Временная заглушка
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class NameSlugMixin(models.Model):
    """Миксин для полей name и slug."""

    name = models.CharField(
        max_length=settings.MAX_CHAR_LEN, verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=settings.MAX_SLUG_LEN, verbose_name='Слаг', unique=True,
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
        max_length=settings.MAX_CHAR_LEN, verbose_name='Название произведения',
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
        Genres, related_name='titles', verbose_name='Жанр произведения'
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


class Reviews(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    text = models.CharField(
        max_length=200,
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    score = models.IntegerField(
        verbose_name='оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'}
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='Ограничение на уникальность'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comments(models.Model):
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    text = models.CharField(
        verbose_name='текст комментария',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
