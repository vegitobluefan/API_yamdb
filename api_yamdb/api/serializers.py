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
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def create(self, validated_data):
        def return_response(msg):
            raise serializers.ValidationError(msg)
        if (
            User.objects.filter(username=validated_data['username']).exists()
            and User.objects.filter(email=validated_data['email']).exists()
        ):
            user = User.objects.get(username=validated_data['username'],
                                    email=validated_data['email'])
            return user

        if User.objects.filter(email=validated_data['email']).exists():
            return_response("Пользователь с таким email уже существует.")

        if User.objects.filter(username=validated_data['username']).exists():
            return_response("Пользователь с таким username уже существует.")

        if validated_data['username'] == 'me':
            raise serializers.ValidationError(
                'Выберите другой username')

        user = User.objects.create(**validated_data)
        return user

    def validate(self, data):

        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Выберите другой username')

        if len(data['email']) > MAX_EMAIL_LEN:
            raise serializers.ValidationError(
                'Email слишком длинный')

        if len(data['username']) > MAX_USERNAME_LEN:
            raise serializers.ValidationError(
                'Имя пользователя слишком длинное')

        pattern = re.compile(r'^[\w.@+-]+\Z')

        if not re.match(pattern, data['username']):
            raise serializers.ValidationError(
                'Имя пользователя включает запрещенные символы')

        return data


class UserAccessTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            user, data['confirmation_code']
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data
