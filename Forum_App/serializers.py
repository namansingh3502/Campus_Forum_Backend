from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    body = serializers.CharField(source='post.body', read_only=True)
    time = serializers.DateTimeField(source='post.time', read_only=True)
    media_count = serializers.IntegerField(source='post.media_count', read_only=True)

    class Meta:
        model = User_Post_Media
        fields = [
            'user_id',
            'username',
            'post_id',
            'body',
            'time',
            'media_count',
        ]


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Post_Comment
        fields = ('post', 'username', 'datetime', 'body')


class LikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Post_Like
        fields = ('username', 'user_id')


class ChannelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('name', )
