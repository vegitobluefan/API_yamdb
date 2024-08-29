from api_yamdb.urls import API_VERSION
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, get_token, registration

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(f'{API_VERSION}/signup', registration),
    path(f'{API_VERSION}/token', get_token),
    path(f'{API_VERSION}/', include(router.urls)),
]
