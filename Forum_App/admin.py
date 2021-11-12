from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(PostDetail)
class Post_Detail_Admin(admin.ModelAdmin):
    list_display = ('user','time',)

    list_filter = ('is_active',)


'''@admin.register(PostDetail)
class Post_Detail_Admin(admin.ModelAdmin):
    list_display = ('user','time',)

    list_filter = ('is_active',)

    fieldsets = (
        ('Post Visibility', {
            'fields': ('is_active',)
        }),
    )

    readonly_fields = ['user', 'time', 'body', 'image_count']'''

@admin.register(PostComment)
class Post_Comment_Admin(admin.ModelAdmin):
    list_display = ('post', 'user', 'datetime', 'is_active')

    list_filter = ('is_active',)

    fieldsets = (
        ('Comment Visibility',{
            'fields':('is_active',)
        }),
    )

    readonly_fields = ['post', 'user', 'datetime', 'body']

@admin.register(ChannelDetail)
class Channel_Detail_List(admin.ModelAdmin):
    list_display = ('channel_name','channel_admin_1','channel_admin_2')

    fieldsets = (
        ('Channel Detail',{
            'fields': ('channel_name','channel_admin_1','channel_admin_2')
         }),
    )

    add_fieldsets = (
        ('Channel Detail',{
            'fields': ( 'channel_admin_1', 'channel_admin_2')
        }),
    )
