from django.shortcuts import render
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User."""

    pass


def registration():
    """Функция для регистрации."""
    pass


def get_token():
    """Функция для получения токена"""
    pass
