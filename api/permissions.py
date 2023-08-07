# DRF import
from rest_framework.permissions import IsAuthenticated

# import models
from user.models.user import MyUser


class CurrentUserPermission(IsAuthenticated):
    ''' is user make update or not '''
    def has_object_permission(self, request, view, obj):
        # Разрешить только чтение всем
        # Разрешить доступ админам для всех остальных методов
        return request.user and request.user.is_superuser
