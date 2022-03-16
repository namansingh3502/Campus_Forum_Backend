from django.contrib import admin

from .models import *

# Register your models here.


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'is_active')

    list_filter = ('is_active',)

    fieldsets = (
        ('Channel Details', {
            'fields': ('name', 'admin', 'is_active', 'moderator')
        }),
    )

    filter_horizontal = ('moderator',)


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
            'fields': ('body', 'posted_in')
        }),
        ('Additional Details', {
            'fields': ('time', 'media_count')
        }),
        ('Visibility', {
            'fields': ('is_hidden',)
        })
    )

    readonly_fields = ('time', 'media_count', 'posted_in', 'body')


@admin.register(Post_Comment)
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


@admin.register(Post_Like)
class PostLikeAdmin(admin.ModelAdmin):

    list_display = ('user', 'post')

    fieldsets = (
        ('Like Details', {
            'fields': ('user', 'post', 'time')
        }),
    )

    readonly_fields = ('time', 'user', 'post')


@admin.register(User_Post_Media)
class UserPostMedia(admin.ModelAdmin):

    list_display = ('user', 'post')

    fieldsets = (
        ('User Post Details ', {
            'fields': ('user', 'post', 'media')
        }),
    )

    readonly_fields = ('user', 'post', 'media')
