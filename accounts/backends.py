from django.contrib.auth.backends import ModelBackend
from .models import CustomUser


class BaseCustomUserBackend(ModelBackend):

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id, is_active=True)
        except CustomUser.DoesNotExist:
            return None


class PhoneBackend(BaseCustomUserBackend):

    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(phone=phone, is_active=True)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None


class UsernameBackend(BaseCustomUserBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(phone=username, is_active=True)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

