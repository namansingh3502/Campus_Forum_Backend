from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'is_active', 'is_staff', 'is_superuser')

    list_filter = ('groups', 'is_staff', 'is_superuser')

    fieldsets = (
        ('Profile', {
            'fields': (
                'username',
                'first_name',
                'middle_name',
                'last_name',
                'gender',
                'department',
                'email',
                'phone',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': (
                'last_login',
                'date_joined'
            )
        }),
    )

    add_fieldsets = (
        ('Authentication Details', {
            'fields': (
                'username',
                'password1',
                'password2'
            )
        }),
        ('Profile', {
            'fields': (
                'first_name',
                'middle_name',
                'last_name',
                'gender',
                'email',
                'phone',
                'user_image',
                'cover_photo'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')

