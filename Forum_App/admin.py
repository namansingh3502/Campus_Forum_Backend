from django.contrib import admin

from .models import *

# Register your models here.


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'is_active')

    list_filter = ('is_active',)

    fieldsets = (
        ('Channel Details', {
            # 'fields': ('is_active', 'name', 'admin', 'moderator')
            'fields': ('is_active', 'name', 'admin')
        }),
        ('Channel Member', {
            # 'fields': ('members','moderator')
            'fields': ('members',)
        }),
    )

    # filter_horizontal = ('moderator', 'members')
    filter_horizontal = ('members',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('pk', 'time', 'is_hidden', 'is_edited')

    search_fields = ('pk',)

    list_filter = ('is_hidden', 'is_edited')

    fieldsets = (
        ('Post Details', {
            'fields': ('is_hidden', 'is_edited', 'posted_in', 'time', 'body')
        }),
    )

    readonly_fields = ('posted_in', 'time', 'body', 'is_edited' )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PostComments)
class PostCommentAdmin(admin.ModelAdmin):

    list_display = ('post', 'user', 'is_hidden')

    search_fields = ('post__pk', 'user__username')

    list_filter = ('is_hidden', )

    fieldsets = (
        ('Comment Details', {
            'fields': ('is_hidden', 'post', 'user', 'time', 'body')
        }),
    )

    readonly_fields = ('post', 'user', 'time', 'body')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PostLikes)
class PostLikeAdmin(admin.ModelAdmin):

    list_display = ('user', 'post')

    search_fields = ('post__pk', 'user__username')

    fieldsets = (
        ('Like Details', {
            'fields': ('user', 'post')
        }),
    )

    readonly_fields = ('post', 'user')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(UserPostMedia)
class UserPostMedia(admin.ModelAdmin):

    list_display = ('user', 'post', 'media')

    search_fields = ('post__pk', 'user__username')

    fieldsets = (
        ('User Post Details ', {
            'fields': ('user', 'post', 'media')
        }),
    )

    readonly_fields = ('user', 'post', 'media')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
