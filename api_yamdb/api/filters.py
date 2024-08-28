from django_filters import rest_framework

from reviews.models import Titles


class TitleFilter(rest_framework.FilterSet):
    """Фильтртрация для модели Titles."""

    category = rest_framework.CharFilter(
        field_name="category__slug",
    )
    genre = rest_framework.CharFilter(field_name="genre__slug",)

    class Meta:
        model = Titles
        fields = ('name', 'year',)
