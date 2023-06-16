"""Маршруты приложения api."""
from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (GroupListRetrieveViewSet,  # isort: skip
                       PostViewSet,  # isort: skip
                       CommentViewSet,
                       FollowListCreateViewSet)  # isort: skip


# Версия API
API_VERSION = settings.API_VERSION

router = DefaultRouter()
router.register('groups', GroupListRetrieveViewSet)
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet,
                basename='comments')
router.register('follow', FollowListCreateViewSet, basename='follow')

urlpatterns = [
    path(f'{API_VERSION}/', include('djoser.urls.jwt')),
    path(f'{API_VERSION}/', include(router.urls)),
]
