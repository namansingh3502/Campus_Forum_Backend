from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

@admin.register(UserProfile)
class User_Profile_Admin(UserAdmin):
    list_display = ('username', )

    list_filter = ('groups',)

    fieldsets = (
        ('Profile', {
            'fields': (
                'username',
                'prefix',
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
            'prefix',
            'first_name',
            'middle_name',
            'last_name',
            'gender',
            'email',
            'phone',
            'user_image')
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

    filter_horizontal = ('groups','user_permissions')

