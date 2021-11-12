from rest_framework import serializers
from .models import *

class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostDetail
        fields=('user','time','body')

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostComment
        fields=('post','user','datetime', 'body')

class ChannelListSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChannelDetail
        fields=('channel_name')
