from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Пользовательское разрешение, позволяющее редактировать
    или удалять объект только владельцам.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, request.user.__class__):
            return obj == request.user
        return False
