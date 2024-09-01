from django.core.exceptions import ValidationError
from rest_framework import serializers
from reviews.models import (Categories, Genres, Titles, Reviews, Comments)


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Categories."""

    class Meta:
        model = Categories
        fields = ('name', 'slug',)


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genres
        fields = ('name', 'slug',)


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        write_only=True,
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug',
        write_only=True,
    )

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)


class ReviewsSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Reviews


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
        model = Comments
