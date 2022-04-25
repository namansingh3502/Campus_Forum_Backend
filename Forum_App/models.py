from django.db import models
from django.utils.translation import gettext_lazy as _


class Channel(models.Model):
    """
    Information related to Channel.
    All fields are required.
    """

    name = models.CharField(_("Channel Name"), max_length=50, blank=False, null=False, unique=True)
    is_active = models.BooleanField(
        _('Is active'),
        default=True,
        help_text=
        _('Designates whether this channel should be treated as active. '
          'Unselect this instead of deleting channels.'),
        null=False,
        blank=False
    )
    admin = models.ForeignKey(
        'AuthenticationApp.UserProfile',
        on_delete=models.CASCADE,
        related_name='Channel_Admin'
    )
    members = models.ManyToManyField(
        to="AuthenticationApp.UserProfile",
        verbose_name=_("Channel Member")
    )
    moderator = models.ManyToManyField(
        to='AuthenticationApp.UserProfile',
        related_name=_("Moderator")
    )

    class Meta:
        db_table = "channel"
        verbose_name = _("channel")
        verbose_name_plural = _("channels")
        unique_together = ('name', 'admin')

    def __str__(self):
        return self.name


class Post(models.Model):
    """
        Information related to post.
    """

    body = models.TextField("Post text", blank=True, null=False)
    time = models.DateTimeField(blank=False, auto_now=True)

    is_hidden = models.BooleanField(
        'Is Hidden',
        default=False,
        help_text=
        'Designates whether this post should be treated as hidden.'
        'Unselect this instead of deleting post.'
    )

    posted_in = models.ManyToManyField(
        to="Channel",
        related_name="Post_Channel"
    )
    is_edited = models.BooleanField(
        default=False,
        blank=False,
        null=False
    )

    class Meta:
        db_table = "post"
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return "Post-Id : %s" % self.pk


class PostLikes(models.Model):
    user = models.ForeignKey(
        'AuthenticationApp.UserProfile',
        on_delete=models.CASCADE,
        related_name='User_Liked'
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='Liked_Post'
    )

    class Meta:
        db_table = "post_likes"
        verbose_name = _("like")
        verbose_name_plural = _("likes")
        unique_together = ('user', 'post')

    def __str__(self):
        return "%s %s" % (self.user, self.post)


class PostComments(models.Model):
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

    body = models.TextField("Comment", blank=False, null=False)
    time = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(
        'Is Hidden',
        default=False,
        help_text=
        'Designates whether this comment should be treated as visible. '
        'Unselect this instead of deleting comment.'
    )

    class Meta:
        db_table = "post_comment"
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return "%s %s" % (self.user, self.post)


class Media(models.Model):
    file = models.URLField(
        "File Path",
    )

    file_type = models.CharField(
        "File Type ",
        max_length=10
    )

    def __str__(self):
        return str(self.pk)


class UserPostMedia(models.Model):
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

    class Meta:
        db_table = "post_user_media"
        verbose_name = _("post_User_Media")
        verbose_name_plural = _("post_user_media")
        unique_together = ('user', 'post', 'media')

    def __str__(self):
        link = "%s %s %s" % (self.user, self.post_id, self.media)
        return link
