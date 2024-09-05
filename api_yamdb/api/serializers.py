import re

from api_yamdb.settings import MAX_EMAIL_LEN, MAX_USERNAME_LEN
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Categories."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        write_only=True,
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        write_only=True,
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)


class TitleRatingSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title, добавлен Rating."""

    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating',
        )


class ReviewsSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title_id = self.context['view'].kwargs["title_id"]
            author = self.context['request'].user
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Нельзя создавать несколько отзывов на произведение'
                )
        return data

    class Meta:
        fields = (
            'id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'id', 'text', 'author', 'pub_date', 'review')
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'bio',
            'role'
        )


class UserCreateSerializer(serializers.Serializer):
    """Сериализатор для создания User."""
    email = serializers.EmailField(required=True,
                                   max_length=MAX_EMAIL_LEN)
    username = serializers.CharField(required=True,
                                     max_length=MAX_USERNAME_LEN)

    def return_response(self, msg):
        """Метод для dry."""
        raise serializers.ValidationError(msg)

    def validate(self, data):
        """Валидатор."""
        if data['username'] == 'me':
            self.return_response(
                'Выберите другой username')

        pattern = re.compile(r'^[\w.@+-]+\Z')

        if not re.match(pattern, data['username']):
            self.return_response(
                'Имя пользователя включает запрещенные символы')

        if (
            User.objects.filter(username=data['username']).exists()
            and User.objects.filter(email=data['email']).exists()
            ):
            return data

        if User.objects.filter(email=data['email']).exists():
            self.return_response("Пользователь с таким email уже существует.")

        if User.objects.filter(username=data['username']).exists():
            self.return_response(
                "Пользователь с таким username уже существует.")
        return data


class UserAccessTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(required=True,
                                     max_length=MAX_USERNAME_LEN)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            user, data['confirmation_code']
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data
