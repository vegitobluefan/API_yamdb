from api_yamdb.urls import API_VERSION
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet, ReviewsViewSet, CommentsViewSet

router = SimpleRouter()
router.register('genres', GenresViewSet, basename='genres')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('titles', TitlesViewSet, basename='titles')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path(f'{API_VERSION}/', include(router.urls)),
]
