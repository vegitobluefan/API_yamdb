from django_filters import rest_framework

from reviews.models import Title


class TitlesFilter(rest_framework.FilterSet):
    """Фильтртрация для модели Titles."""

    category = rest_framework.CharFilter(
        field_name="category__slug",
    )
    genre = rest_framework.CharFilter(field_name="genre__slug",)

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre',)
