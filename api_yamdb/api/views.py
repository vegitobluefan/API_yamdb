from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination


class CategoriesViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Categories."""

    pass


class GenresViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Genres."""

    pass


class TitlesViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Titles."""

    pass
