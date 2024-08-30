from api_yamdb.urls import API_VERSION
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, get_token, registration

app_name = 'users'

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(f'{API_VERSION}/auth/signup/', registration),
    path(f'{API_VERSION}/auth/token/', get_token),
    path(f'{API_VERSION}/', include(router.urls)),
]
