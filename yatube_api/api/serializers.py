"""Серриализаторы приложения api."""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from posts.models import Comment, Post, Group, Follow  # isort: skip

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    """Серриализатор групп."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    """Серриализатор постов."""
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
    """Серриализатор подписок на авторов."""
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    following = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def to_internal_value(self, data):
        # Проверяем обязательное поле following
        if not data.get('following'):
            raise ValidationError({'following': ['Обязательное поле.']})

        user = self.context.get('request').user
        # Проверяем существует ли пользователь, на котрого
        # запрашивается подписка. Со встроенным методом get_object_or_404
        # не проходит тест на некорретные данные.
        try:
            following = User.objects.get(username=data.get('following'))
        except User.DoesNotExist:
            raise ValidationError({'message':
                                   f'Пользователь {following} не найден.'})

        # Проверяем что подписка не на самого себя
        if user == following:
            raise ValidationError(
                {'message': 'Подписка на самого себя запрещена.'})

        # Возвращаем объект User, вместо строки для того чтобы
        # в методе perform_create второй раз не получать его из БД
        return {'following': following}
