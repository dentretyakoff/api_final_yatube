"""Вьюсеты приложения api."""
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from posts.models import Group, Post  # isort: skip
from api.permissions import IsAuthor  # isort: skip
from api.serializers import (GroupSerializer,  # isort: skip
                             PostSerializer,  # isort: skip
                             CommentSerializer,  # isort: skip
                             FollowSerializer)  # isort: skip


class GroupListRetrieveViewSet(mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               viewsets.GenericViewSet):
    """Получает группы списком или по одной."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Позволяет выполнять все операции CRUD с постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthor)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Позволяет выполнять все операции CRUD с комментариями к постам."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthor)

    def get_post(self):
        """Вспомогательный метод для получения поста."""
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowListCreateViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    """Получает подписки пользователя, создает подписку."""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        # Получаем пользвоателей
        user = self.request.user
        following = serializer.validated_data.get('following')

        # Проверяем что подписка уже существует
        if user.follower.filter(following=following).exists():
            raise ValidationError({'message': 'Подписка уже существует.'})

        serializer.save(user=user, following=following)
