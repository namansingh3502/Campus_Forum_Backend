from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user', read_only=True)
    id = serializers.CharField(source='pk', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'username', 'time', 'body', 'media_count']


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Post_Comment
        fields = ('post', 'username', 'datetime', 'body')


class LikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Post_Like
        fields = ('username',)


class ChannelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('name',)
