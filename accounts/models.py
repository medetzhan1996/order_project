from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, phone, date_of_birth, password, **extra_fields):
        user = self.model(
            phone=phone,
            date_of_birth=date_of_birth,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, date_of_birth, password, **extra_fields):
        """Создание и возврат суперпользователя с заданными данными."""
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self.create_user(phone, date_of_birth, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(unique=True, max_length=15)
    date_of_birth = models.DateField()
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['date_of_birth']