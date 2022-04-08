from rest_framework import serializers
from .models import *
from AuthenticationApp.models import *


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'prefix',
            'first_name',
            'middle_name',
            'last_name',
            'user_image'
        ]


class ChannelDetailsSerializer(serializers.ModelSerializer):

    admin = UserDetailsSerializer('admin')
    member_count = serializers.IntegerField(source='members.count', read_only=True)

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
        fields = [
            'username',
            'user_id',
        ]


class PostDataSerializer(serializers.ModelSerializer):
    posted_in = PostChannelSerializer(many=True)
    likes = serializers.SerializerMethodField("getLikes")
    comments_count = serializers.SerializerMethodField("getCommentCount")


    class Meta:
        model = Post
        fields = [
            'id',
            'body',
            'time',
            'media_count',
            'posted_in',
            'likes',
            'comments_count'
        ]

    def getCommentCount(self, post):
        count = post.Commented_Post.count()
        return count

    def getLikes(self, post):
        likes = Post_Like.objects.filter(pk=post.pk).all()
        serializer = LikeSerializer( likes, many=True)
        return serializer.data

class MediaDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ('file',)


class PostSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField("getUser")
    post = serializers.SerializerMethodField("getPost")
    media = serializers.SerializerMethodField("getMedia")

    class Meta:
        fields = [
            'user',
            'post',
            'media',
        ]

    def getUser(self, post):
        user = post.Post.all()[0].user
        serializers = UserDetailsSerializer(user)
        return serializers.data

    def getPost(self, post):
        serializers = PostDataSerializer(post)
        return serializers.data


    def getMedia(self, post):
        media_file = post.Post.filter(media_id__isnull = False).order_by('pk')

        media_list=[]
        if media_file :
            media_list = list(map(lambda x: x.media, media_file))

        serializer = MediaDataSerializer(media_list, many=True)
        return serializer.data


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