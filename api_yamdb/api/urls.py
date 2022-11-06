import api.views
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', api.views.CategoriesViewSet,
                basename='categories')
router.register(r'genres', api.views.GenresViewSet, basename='genres')
router.register(r'titles', api.views.TitlesViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', api.views.ReviewsViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    api.views.CommentsViewSet, basename='comments')
router.register(r'users', api.views.UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    # path('auth/, ),    # auth/signup
    path('v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
]
