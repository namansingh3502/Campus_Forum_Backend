from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Admin page settings

admin.site.site_header = 'College Forum'
admin.site.index_title = 'Features area'
admin.site.site_title = 'HTML title from Administration'


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
                # 'groups',
                # 'user_permissions'
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
                # 'groups',
                # 'user_permissions'
            )
        }),
    )

    # filter_horizontal = ('groups', 'user_permissions')

