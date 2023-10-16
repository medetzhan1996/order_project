from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('phone', 'date_of_birth', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('phone',)
    ordering = ('phone',)
    readonly_fields = ('phone',)
    change_password_form = AdminPasswordChangeForm

    fieldsets = (
        (None, {'fields': ('phone', 'date_of_birth', 'profile_photo')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Password'), {'fields': ('password',)}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('phone', 'date_of_birth', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
