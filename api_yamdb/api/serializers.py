from rest_framework import serializers
from reviews.models import (Categories, Genres, Titles,)


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
