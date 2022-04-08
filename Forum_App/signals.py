from django.dispatch import receiver
from .models import *

from django import dispatch

media_saved = dispatch.Signal()


@receiver(media_saved)
def media_save_handler(sender, **kwargs):
    User_Post_Media.objects.create(
                    user_id=kwargs['user'],
                    post_id=kwargs['post'],
                    media_id=kwargs['media']
                )
