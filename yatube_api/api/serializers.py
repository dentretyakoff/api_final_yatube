"""Сериализаторы приложения api."""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        read_only=True, slug_field='username')

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def to_internal_value(self, data):
        user = self.context.get('request').user
        following = data.get('following')

        # Проверяем обязательное поле following
        if not following:
            raise ValidationError({'following': ['Обязательное поле.']})

        # Проверяем существует ли пользователь, на которого
        # запрашивается подписка. Со встроенным методом get_object_or_404
        # не проходит тест на некорректные данные.
        try:
            following = User.objects.get(username=following)
        except User.DoesNotExist:
            raise ValidationError({'message':
                                   f'Пользователь {following} не найден.'})

        # Проверяем что подписка не на самого себя
        if user == following:
            raise ValidationError(
                {'message': 'Подписка на самого себя запрещена.'})

        # Проверяем что подписка уже существует
        if user.follower.filter(following=following).exists():
            raise ValidationError({'message': 'Подписка уже существует.'})

        # Возвращаем объект User, вместо строки для того чтобы
        # в методе perform_create второй раз не получать его из БД
        return {'following': following}
