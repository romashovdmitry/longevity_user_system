from rest_framework.permissions import IsAdminUser

from user.models.user import MyUser


class CurrentUserPermission(IsAdminUser):
    ''' is user make update or not '''
    def has_object_permission(self, request, view, obj):
        # Разрешить только чтение всем
        # Разрешить доступ админам для всех остальных методов
        return obj == request.user or request.user.is_superuser is True
