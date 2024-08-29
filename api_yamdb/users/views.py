from rest_framework import status, viewsets
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserAccessTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    """Функция для регистрации."""
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']

    if (User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists()):
        return Response(status=status.HTTP_400_BAD_REQUEST, data="User already exists. Change email and username")

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
@permission_classes([AllowAny])
def get_token(request):
    """Функция для получения токена"""

    serializer = UserAccessTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    user = get_object_or_404(User, username=username)
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)
