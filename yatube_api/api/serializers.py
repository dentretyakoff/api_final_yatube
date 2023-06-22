"""Сериализаторы приложения api."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Comment, Post, Group, Follow  # isort: skip

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор групп."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор постов."""
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')


class CommentSerializer(serializers.ModelSerializer):
    """Серриализатор комментариев к постам."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок на авторов."""
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        user = self.context.get('request').user
        following = data.get('following')

        # Если подписка существует выбрасываем исключение
        if user.follower.filter(following=following).exists():
            raise serializers.ValidationError(
                {'message': 'Подписка уже существует.'})

        # Проверяем что подписка не на самого себя
        if user == following:
            raise serializers.ValidationError(
                {'message': 'Подписка на самого себя запрещена.'})

        return data
