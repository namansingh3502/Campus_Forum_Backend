from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Post_Detail)
class Post_Detail_Admin(admin.ModelAdmin):
    list_display = ('')
