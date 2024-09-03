from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import SAFE_METHODS
from reviews.models import Category, Genre, Review, Title

from .filters import TitlesFilter
from .permissions import (AdminOrSuperuserOrReadOnly,
                          AuthenticatedAndAdminOrAuthorOrReadOnly)
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, ReviewsSerializer,
                          TitleRatingSerializer, TitlesSerializer)


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

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(CategoriesGenresMixin):
    """ViewSet для модели Genres."""

    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Titles."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
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
    permission_classes = (AuthenticatedAndAdminOrAuthorOrReadOnly,)
    http_method_names = ('get', 'post', 'head', 'patch', 'delete',)

    def get_title(self):
        title = get_object_or_404(
            Title,
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
    permission_classes = (AuthenticatedAndAdminOrAuthorOrReadOnly,)
    http_method_names = ('get', 'post', 'head', 'patch', 'delete',)

    def get_review(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
