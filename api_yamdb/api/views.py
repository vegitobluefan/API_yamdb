from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPaginations
from reviews.models import Categories, Genres, Titles, Reviews
from django.shortcuts import get_object_or_404
from rest_framework.permissions import SAFE_METHODS
from reviews.models import Categories, Genres, Titles

from .filters import TitlesFilter
from .permissions import AdminOrSuperuserOrReadOnly
from .serializers import (CategoriesSerializer, GenresSerializer, TitleRatingSerializer,
                          TitlesSerializer, ReviewsSerializer, CommentsSerializer)





class CategoriesGenresMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Миксин для повторяющегося кода."""

    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
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
    permission_classes = (AdminOrSuperuserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filterset_class = TitlesFilter
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    ordering = ('id',)
    http_method_names = ('get', 'post', 'head', 'patch', 'delete',)

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return TitlesSerializer
        return TitleRatingSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Reviews."""

    serializer_class = ReviewsSerializer
    permission_classes = (AdminOrAuthorOrReadOnly,)

    def get_title(self):
        title = get_object_or_404(
            Titles,
            id=self.kwargs.get('title_id'))
        return title

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentsViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comments."""

    serializer_class = CommentsSerializer
    permission_classes = (AdminOrAuthorOrReadOnly,)

    def get_review(self):
        review = get_object_or_404(
            Reviews,
            id=self.kwargs.get('review_id'))
        return review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
