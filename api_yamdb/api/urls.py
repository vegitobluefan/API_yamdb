from api_yamdb.urls import API_VERSION
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

router = SimpleRouter()
router.register('genres', GenresViewSet, basename='genres')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path(f'{API_VERSION}/', include(router.urls)),
]
