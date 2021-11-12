import os
from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.

class PostDetail(models.Model):
    """
    necessary information related to posts i.e.
    who created , when created and body/text of post
    """
    user = models.ForeignKey(
        'AuthenticationApp.UserProfile',
        on_delete=models.CASCADE
    )
    time = models.DateTimeField(
        "Post-Time",
        auto_now=True
    )
    body = models.CharField(
        "Post-Text",
        max_length=200,
        blank=True,
        null=True
    )
    image_count = models.PositiveIntegerField(
        "Number of images attached to post",
        default=0,
        null=False,
        blank=False
    )
    is_active = models.BooleanField(
        "Is_Active",
        default=True,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.user.user_id + " " + str(self.time) + " " + str(self.is_active)

class PostImageStore(models.Model):
    """
    images uploaded in posts are stored here
    """

    def path_and_rename(instance):
        path = "userimage/"
        filename = now.strftime("%d_%m_%Y__%H_%M_%S")
        file_extension = filename.split('.')[-1]
        format = str(instance) + "_" + filename + '.' + file_extension
        return os.path.join(path, format)

    image = models.FileField(
        "Post Image",
        upload_to=path_and_rename,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.image

class PostImage(models.Model):
    """
    Relation of post and images is stored here
    """

    post = models.ForeignKey(
        "PostDetail",
        on_delete=models.CASCADE,
        related_name="Post_Id"
    )
    image = models.ForeignKey(
        "PostImageStore",
        on_delete=models.CASCADE,
        related_name="Post_Image_details"
    )

    def __str__(self):
        return self.post + " " + self.image

class PostLike(models.Model):
    """
    Handles details of likes on each post by users
    """

    post = models.ForeignKey(
        "PostDetail",
        on_delete=models.CASCADE,
        related_name="Post_Like"
    )
    user = models.ForeignKey(
        "AuthenticationApp.UserProfile",
        on_delete=models.CASCADE,
        related_name="User_Like"
    )

    def __str__(self):
        return self.post.id + " " + self.user

class PostComment(models.Model):
    """
    Handles details of Comment
    which user commented on which post and when and what
    """

    post = models.ForeignKey(
        "PostDetail",
        on_delete=models.CASCADE,
        related_name="Post_Comment"
    )
    user = models.ForeignKey(
        "AuthenticationApp.UserProfile",
        on_delete=models.CASCADE,
        related_name="User_Comment"
    )
    datetime = models.DateTimeField(
        auto_now=True
    )
    body = models.TextField(
        max_length=100,
        null=False,
        blank=False
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.post + " " + self.user + " " + self.datetime

class ChannelDetail(models.Model):

    channel_name = models.CharField(
        "Channel Name",
        max_length=20,
        null=False,
        blank=True
    )
    channel_admin_1 = models.ForeignKey(
        'AuthenticationApp.UserProfile',
        on_delete=models.CASCADE,
        related_name="Admin_1"
    )
    channel_admin_2 = models.ForeignKey(
        'AuthenticationApp.UserProfile',
        on_delete=models.CASCADE,
        related_name="Admin_2"
    )

    def __str__(self):
        return self.channel_name
