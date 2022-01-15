import os
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ValidationError


# Create your models here.

class Channel(models.Model):
    """
    Information related to Channel.
    All fields are required.
    """

    name = models.CharField("Channel Name", max_length=50, blank=False, null=False, unique=True)
    is_active = models.BooleanField(
        'Is active',
        default=True,
        help_text=
            'Designates whether this channel should be treated as active. '
            'Unselect this instead of deleting channels.'
    )
    admin = models.ForeignKey(
        'AuthenticationApp.UserProfile',
        on_delete=models.CASCADE,
        related_name='Channel_Admin'
    )

    moderator = models.ManyToManyField(
        'AuthenticationApp.UserProfile',
        related_name="Moderator"
    )

    class Meta:
        unique_together = ('name', 'admin',)

    def __str__(self):
        return self.name

class Post(models.Model):
    """
        Information related to posts.
    """

    body = models.TextField("Post text", blank=True)
    time = models.DateTimeField(blank=False, auto_now=True)
    media_count = models.PositiveSmallIntegerField("Media count",default=0, blank=False);

    is_hidden = models.BooleanField(
        'Is Hidden',
        default=False,
        help_text=
        'Designates whether this post should be treated as hidden.'
        'Unselect this instead of deleting post.'
    )

    posted_in = models.ManyToManyField(
        "Channel",
        related_name="Post_Channel",
    )

    def __str__(self):
        return "Post-Id : " + str(self.pk)

class Post_Like(models.Model):

    user = models.ForeignKey(
        'AuthenticationApp.UserProfile',
        related_name='User_liked',
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        'Post',
        related_name='Liked_Post',
        on_delete=models.CASCADE
    )
    time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return str(self.user) + " " + str(self.post)

class Post_Comment(models.Model):
    user = models.ForeignKey(
        'AuthenticationApp.UserProfile',
        related_name='User_Commented',
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        'Post',
        related_name='Commented_Post',
        on_delete=models.CASCADE
    )

    body = models.TextField("Comment", blank=False)
    time = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(
        'Is Hidden',
        default=False,
        help_text=
            'Designates whether this comment should be treated as visible. '
            'Unselect this instead of deleting comment.'
    )

    def __str__(self):
        return str(self.user) + " " + str(self.post)

class Media(models.Model):

    def path_and_rename(instance):
        path = "postimages/"
        filename = now.strftime("%d_%m_%Y__%H_%M_%S")
        file_extension = filename.split('.')[-1]
        format = str(instance) + "_" + filename + '.' + file_extension
        return os.path.join(path, format)

    file_name = models.FileField(
        "Media file",
        upload_to=path_and_rename,
    )

    file_type = models.CharField(
        "File Type ",
        default="image",
        max_length=5
    )

    def __str__(self):
        return self.pk


class User_Post_Media(models.Model):

    user = models.ForeignKey(
        'AuthenticationApp.UserProfile',
        related_name='User',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    post = models.ForeignKey(
        'Post',
        related_name='Post',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    media = models.ForeignKey(
        'Media',
        related_name='Media',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.user)+"-"+str(self.post_id)+"-"+str(self.media)