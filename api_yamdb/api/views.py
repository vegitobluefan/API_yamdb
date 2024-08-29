from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Categories, Genres, Titles

from .filters import TitlesFilter
from .permissions import AdminOrAuthorOrReadOnly, AdminOrSuperuserOrReadOnly
from .serializers import (CategoriesSerializer, GenresSerializer,
                          TitlesSerializer)


class CategoriesGenresMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Миксин для повторяющегося кода."""

    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrSuperuserOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name',)
    ordering = ('id',)


class CategoriesViewSet(CategoriesGenresMixin):
    """ViewSet для модели Categories."""

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(CategoriesGenresMixin):
    """ViewSet для модели Genres."""

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Titles."""

    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (AdminOrAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filterset_class = TitlesFilter
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    ordering = ('id',)
