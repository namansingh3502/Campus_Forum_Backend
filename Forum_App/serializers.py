from rest_framework import serializers
from .models import *
from AuthenticationApp.models import *


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username'
        ]


class ChannelDetailsSerializer(serializers.ModelSerializer):

    admin = UserDetailsSerializer('admin')
    member_count = serializers.IntegerField(source='userprofile_set.count', read_only=True)

    class Meta:
        model = Channel
        fields = [
            'id',
            'name',
            'admin',
            'member_count'
        ]


class PostChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = [
            'id',
            'name'
        ]


class PostDataSerializer(serializers.ModelSerializer):
    channel_name = PostChannelSerializer(source='posted_in', many=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'body',
            'time',
            'media_count',
            'channel_name'
        ]


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    post_data = PostDataSerializer(source='post')

    class Meta:
        model = User_Post_Media
        fields = [
            'user_id',
            'username',
            'post_data'
        ]


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Post_Comment
        fields = ('id', 'username', 'time', 'body')


class LikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Post_Like
        fields = ('username', 'user_id')


class ChannelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'name',
            'id'
        ]