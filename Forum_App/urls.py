"""Campus_Forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

urlpatterns = [
    path('posts', views.posts_user, name="posts_user"),
    path('channel-list', views.channels, name="Channel-List"),
    path('new-post', views.new_post, name="New-Post"),
    path('edit-post', views.edit_post, name="Edit-Post"),
    path('new-comment', views.new_comment, name="New-Comment"),
    path('<int:post_id>/comments', views.post_comment, name="Post-Comments"),
    path('<int:post_id>/likes', views.post_likes, name="Post-Likes"),
    path('<int:post_id>/like-post', views.update_post_like, name="Update-Post-Like"),
    path('channel/<int:channel_id>/posts', views.channel_post, name="Channel-Post"),
    path('channel/<int:channel_id>/profile', views.channel_details, name="Channel-Details"),
]
