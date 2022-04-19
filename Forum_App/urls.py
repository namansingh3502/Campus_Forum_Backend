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
    # post api calls
    path('new_post', views.new_post, name="New-Post"),
    path('edit_post', views.edit_post, name="Edit-Post"),
    path('new_comment', views.new_comment, name="New-Comment"),
    path('<int:post_id>/like_post', views.update_post_like, name="Update-Post-Like"),

    # get calls
    path('channel_list', views.channels, name="Channel-List"),
    path('channel/<str:channel_name>/profile', views.channel_details, name="Channel-Details"),


    # paginated query
    path('posts/<int:last_post>', views.posts, name="posts_user"),
    path('user/<str:username>/post/<int:last_post>', views.user_post, name="User-Post"),
    path('channel/<str:channel_name>/post/<int:last_post>', views.channel_post, name="Channel-Post"),
    path('comment/<int:post_id>/<int:last_comment>', views.post_comment, name="Post-Comments"),
]
