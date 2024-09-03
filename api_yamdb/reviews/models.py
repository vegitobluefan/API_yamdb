from api_yamdb.settings import (MAX_CHAR_LEN, MAX_SLUG_LEN, MAX_VALUE,
                                MIN_VALUE, TEXT_LENGTH)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class NameSlugBaseModel(models.Model):
    """Миксин для полей name и slug."""

    name = models.CharField(
        max_length=MAX_CHAR_LEN, verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=MAX_SLUG_LEN, verbose_name='Слаг', unique=True,
    )

    def __str__(self) -> str:
        return self.title


class TextPubdateBaseModel(models.Model):
    """Миксин для полей text и pubdate."""

    text = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self) -> str:
        return self.text


class Category(NameSlugBaseModel):
    """Модель для категорий произведений."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugBaseModel):
    """Модель для жанров произведений."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель для произведений."""

    name = models.CharField(
        max_length=MAX_CHAR_LEN, verbose_name='Название произведения',
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
    )
    description = models.CharField(
        verbose_name='Описание произведения',
        max_length=MAX_CHAR_LEN,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles', verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
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


class Review(TextPubdateBaseModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    score = models.SmallIntegerField(
        verbose_name='оценка',
        validators=(
            MinValueValidator(MIN_VALUE),
            MaxValueValidator(MAX_VALUE)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'}
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            )]
        ordering = ('pub_date',)


class Comment(TextPubdateBaseModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
