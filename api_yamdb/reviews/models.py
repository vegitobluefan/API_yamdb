from api_yamdb.settings import (MAX_CHAR_LEN, MAX_EMAIL_LEN, MAX_LEN_BIO,
                                MAX_SLUG_LEN, MAX_USERNAME_LEN, MAX_VALUE,
                                MIN_VALUE, TEXT_LENGTH)

from api.utils import validate_username

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator)

from django.db import models


class Roles(models.TextChoices):
    """Класс ролей."""

    USER = 'user', 'Пользователь'
    MODERATOR = 'moderator', 'Модератор'
    ADMIN = 'admin', 'Администратор'


class validate_username_regex(UnicodeUsernameValidator):
    """Валидатор."""
    regex = (r'^[\w.@+-]+\Z')


class User(AbstractUser):
    """Модель для описания пользователя."""
    username_validator = validate_username_regex()

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
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=MAX_USERNAME_LEN,
        unique=True,
        validators=[username_validator, validate_username, ]
    )

    @property
    def is_admin(self):
        return (self.role == Roles.ADMIN
                or self.is_superuser or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == Roles.MODERATOR

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


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
    year = models.SmallIntegerField(
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
    """Модель для отзывов."""

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
    score = models.PositiveSmallIntegerField(
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
    """Модель для комментариев."""

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
