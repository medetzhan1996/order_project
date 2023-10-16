from rest_framework.permissions import BasePermission


class CanCreateOrderPermission(BasePermission):
    """
    Разрешение, которое позволяет создание заказов всем пользователям,
    но изменение и удаление только авторизованным.
    """
    def has_permission(self, request, view):
        if request.method in ['POST', 'GET']:
            return True
        return request.user.is_authenticated


class CanRetrieveOrderPermission(BasePermission):
    """
    Разрешение на доступ к заказу.
    Неавторизованные могут видеть только заказы без пользователя.
    Авторизованные видят свои заказы и заказы без пользователя.
    """

    def has_object_permission(self, request, view, obj):
        # Если у заказа нет пользователя, разрешить доступ
        if not obj.user:
            return True

        # Если пользователь авторизован и является создателем заказа, разрешить доступ
        if request.user.is_authenticated and obj.user == request.user:
            return True

        return False


