from .models import User
from .serializers import (UserSerializer,
                          UserCreateSerializer,
                          UserAccessTokenSerializer)
from api.permissions import IsAdmin

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework import permissions, status, viewsets, filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action, api_view, permission_classes

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


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
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(self.request.user,
                                    data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registration(request):
    """Функция для регистрации."""
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']

    if (User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists()):
        return Response(status=status.HTTP_200_OK)

    if (User.objects.filter(email=email).exists() and not User.objects.filter(username=username).exists()):
        return Response(status=status.HTTP_400_BAD_REQUEST, data="Пользователь с таким email уже существует.")

    if (not User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists()):
        return Response(status=status.HTTP_400_BAD_REQUEST, data="Пользователь с таким username уже существует.")
    status.HTTP_403_FORBIDDEN
    user, code_created = User.objects.get_or_create(
        email=email,
        username=username)

    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()

    try:
        send_mail(
            subject='Confirmation code',
            message=f"Your code - {confirmation_code}",
            from_email=None,
            recipient_list=[email],
            fail_silently=False
        )
    except OSError:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data="Network is unreachable")

    return Response(
        serializer.data,
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
