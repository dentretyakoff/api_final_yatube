"""Вьюсеты приложения api."""
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from posts.models import Group, Post  # isort: skip
from api.permissions import IsAuthor  # isort: skip
from api.serializers import (GroupSerializer,  # isort: skip
                             PostSerializer,  # isort: skip
                             CommentSerializer)  # isort: skip


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
    permission_classes = (IsAuthor,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Позволяет выполнять все операции CRUD с комментариями к постам."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthor,)

    def get_post(self):
        """Вспомогательный метод для получения поста."""
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())
