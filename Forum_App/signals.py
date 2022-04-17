from django.dispatch import receiver
from .models import *

from django import dispatch

media_saved = dispatch.Signal()
post_saved = dispatch.Signal()


@receiver(post_saved)
def post_save_handler(sender, **kwargs):
    UserPostMedia.objects.create(
                    user_id=kwargs['user'],
                    post_id=kwargs['post'],
                    media_id=kwargs['media']
                )


@receiver(media_saved)
def media_save_handler(sender, **kwargs):
    UserPostMedia.objects.create(
                    user_id=kwargs['user'],
                    post_id=kwargs['post'],
                    media_id=kwargs['media']
                )
