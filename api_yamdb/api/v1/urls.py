import api.v1.views
from django.urls import path, include
from rest_framework import routers

from .views import get_token, signup

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', api.v1.views.CategoriesViewSet,
                basename='categories')
router.register(r'genres', api.v1.views.GenresViewSet, basename='genres')
router.register(r'titles', api.v1.views.TitlesViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                api.v1.views.ReviewsViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    api.v1.views.CommentsViewSet, basename='comments')
router.register(r'users', api.v1.views.UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='token_obtain_pair'),
]
