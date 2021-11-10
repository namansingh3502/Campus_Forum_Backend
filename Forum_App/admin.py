from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Post_Detail)
class Post_Detail_Admin(admin.ModelAdmin):
    list_display = ('user','time',)

    list_filter = ('is_active',)

    fieldsets = (
        ('Post Visibility', {
            'fields': ('is_active',)
        }),
    )

    readonly_fields = ['user', 'time', 'body', 'image_count']

@admin.register(Post_Comment)
class Post_Comment_Admin(admin.ModelAdmin):
    list_display = ('post', 'user', 'datetime', 'is_active')

    list_filter = ('is_active',)

    fieldsets = (
        ('Comment Visibility',{
            'fields':('is_active',)
        }),
    )

    readonly_fields = ['post', 'user', 'datetime', 'body']
