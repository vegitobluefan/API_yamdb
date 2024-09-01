from .models import User

from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
import re


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'bio',
            'role'
        )


class UserCreateSerializer(serializers.Serializer):
    """Сериализатор для создания User."""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Выберите другой username')

        if len(data['email']) > 254:
            raise serializers.ValidationError(
                'Email слишком длинный')

        if len(data['username']) > 150:
            raise serializers.ValidationError(
                'Имя пользователя слишком длинное')

        pattern = re.compile(r'^[\w.@+-]+\Z')

        if not re.match(pattern, data['username']):
            raise serializers.ValidationError(
                'Имя пользователя включает запрещенные символы')

        return data


class UserAccessTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            user, data['confirmation_code']
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data
