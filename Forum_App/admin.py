from django.contrib import admin

from .models import *

# Register your models here.


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'is_active')

    list_filter = ('is_active',)

    fieldsets = (
        ('Channel Details', {
            'fields': ('name', 'admin', 'is_active')
        }),
    )


@admin.register(Moderator)
class ModeratorAdmin(admin.ModelAdmin):
    list_display = ('channel',)

    fieldsets = (
        ('Channel Moderators', {
            'fields': ('channel', 'user')
        }),
    )

    filter_horizontal = ('user',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    """
        def has_add_permission(self, request, obj=None):
            return False

        def has_delete_permission(self, request, obj=None):
            return False
    """

    list_display = ('pk', 'time', 'is_hidden')

    list_filter = ('is_hidden', )

    fieldsets = (
        ('Post Details', {
            'fields': ('body', 'posted_in', 'is_hidden')
        }),
        ('Additional Details', {
            'fields': ('time', 'media_count')
        })
    )

    readonly_fields = ('time', 'media_count')

    filter_horizontal = ('posted_in',)


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):

    """
        def has_add_permission(self, request, obj=None):
            return False

        def has_delete_permission(self, request, obj=None):
            return False

    """

    list_display = ('post', 'user', 'is_hidden')

    list_filter = ('is_hidden', )

    fieldsets = (
        ('Comment Details', {
            'fields': ('user', 'post', 'body', 'time')
        }),
        ('Visibility', {
            'fields': ('is_hidden',)
        })
    )

    readonly_fields = ('user', 'post', 'time', 'body')
