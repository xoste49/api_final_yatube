from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

from api.views import PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')


urlpatterns = [
        path(
            'token/',
            TokenObtainPairView.as_view(),
            name='token_obtain_pair'
        ),
        path(
            'token/refresh/',
            TokenRefreshView.as_view(),
            name='token_refresh'
        ),
    ]