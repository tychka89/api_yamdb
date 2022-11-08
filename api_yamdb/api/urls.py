from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView)


app_name = 'api'

v1_router = DefaultRouter()

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    # path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', 
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'), #после v1 можно написать auth/signup/ и что угодно чтоб поменять ендпоинт
]
