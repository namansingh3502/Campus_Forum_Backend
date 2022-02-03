from rest_framework import serializers
from .models import *
from AuthenticationApp.models import *


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'user_image'
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


class LikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Post_Like
        fields = ('username', 'user_id')


class PostDataSerializer(serializers.ModelSerializer):
    posted_in = PostChannelSerializer(many=True)
    Liked_Post = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'body',
            'time',
            'media_count',
            'posted_in',
            'Liked_Post'
        ]


class PostSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)
    post = PostDataSerializer(read_only=True)

    class Meta:
        model = User_Post_Media
        fields = [
            'user',
            'post',
            'media',
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Post_Comment
        fields = ('id', 'user', 'time', 'body')


class ChannelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'name',
            'id'
        ]