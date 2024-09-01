from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from reviews.models import (Category, Genre, Title, Review, Comment)


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
