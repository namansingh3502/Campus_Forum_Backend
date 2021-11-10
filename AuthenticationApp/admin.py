from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

@admin.register(UserProfile)
class User_Profile_Admin(UserAdmin):
    list_display = ('username', )

    list_filter = ('groups',)

    fieldsets = (
        ('Authentication Details', {
            'fields': ('username', 'password')
        }),
        ('Profile', {
            'fields':('prefix', 'first_name','middle_name','last_name', 'user_id', 'email', 'phone', 'address', 'user_image')
        }),
        ('Permissions', {
            'fields': ( 'is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        ('Authentication Details', {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Profile', {
            'fields': (
            'prefix', 'first_name', 'middle_name', 'last_name', 'user_id', 'email', 'phone', 'address', 'user_image')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

