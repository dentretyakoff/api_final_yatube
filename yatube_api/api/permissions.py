"""Классы для авторизации пользователей в приложении api."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthor(BasePermission):
    """Проверяет является ли пользователь автором редактиуемого объекта."""
    def has_object_permission(self, request, view, obj):
        """Проверка авторства."""
        # Для безопасных методов GET, HEAD, OPTIONS разрешаем
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
