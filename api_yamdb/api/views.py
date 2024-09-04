from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets, permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title

from .filters import TitlesFilter
from .permissions import (AdminOrSuperuserOrReadOnly,
                          AuthenticatedAndAdminOrAuthorOrReadOnly,
                          IsAdmin)
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, ReviewsSerializer,
                          TitleRatingSerializer, TitlesSerializer,
                          UserAccessTokenSerializer, UserCreateSerializer,
                          UserSerializer)

from users.models import User


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


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    lookup_field = 'username'
    search_fields = ['username', ]
    http_method_names = ["get", "post", "delete", "patch"]

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
        else:
            serializer = UserSerializer(
                self.request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registration(request):
    """Функция для регистрации."""
    user = UserCreateSerializer(data=request.data)
    user.is_valid(raise_exception=True)
    user.save()
    email = user.data['email']
    username = user.data['username']
    data = user.data
    user = User.objects.get(
        email=email,
        username=username)

    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        subject='Confirmation code',
        message=f"Your code - {confirmation_code}",
        from_email=None,
        recipient_list=[email],
        fail_silently=False
    )
    return Response(
        data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """Функция для получения токена"""

    serializer = UserAccessTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    user = get_object_or_404(User, username=username)
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)
