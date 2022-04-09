from rest_framework import serializers
from .models import *
from AuthenticationApp.models import *


class UserDetailsSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'full_name',
            'user_image',
            'cover_photo'
        ]

    def get_full_name(self, user):
        return "%s %s %s" % (user.first_name, user.middle_name, user.last_name)


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


class ChannelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'name',
            'id'
        ]


class LikeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = PostLikes
        fields = [
            'full_name',
            'user_id',
        ]

    def get_full_name(self, likes):
        user = likes.user
        return "%s %s %s" % (user.first_name, user.middle_name, user.last_name)


class PostDataSerializer(serializers.ModelSerializer):
    posted_in = ChannelListSerializer(many=True)
    likes = serializers.SerializerMethodField("getLikes")
    comments_count = serializers.SerializerMethodField("getCommentCount")

    class Meta:
        model = Post
        fields = [
            'id',
            'body',
            'time',
            'posted_in',
            'likes',
            'comments_count'
        ]

    def getCommentCount(self, post):
        return "%s" % post.Commented_Post.count()

    def getLikes(self, post):
        likes = PostLikes.objects.filter(pk=post.pk).all()
        serializer = LikeSerializer(likes, many=True)
        return serializer.data


class MediaDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ('file',)


class PostSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField("get_user")
    post = serializers.SerializerMethodField("get_post")
    media = serializers.SerializerMethodField("get_media")

    class Meta:
        fields = [
            'user',
            'post',
            'media',
        ]

    def get_user(self, post):
        user = post.Post.all()[0].user
        serializers = UserDetailsSerializer(user)
        return serializers.data

    def get_post(self, post):
        serializers = PostDataSerializer(post)
        return serializers.data


    def get_media(self, post):
        media_file = post.Post.filter(media_id__isnull = False).order_by('pk')

        media_list=[]
        if media_file :
            media_list = list(map(lambda x: x.media, media_file))

        serializer = MediaDataSerializer(media_list, many=True)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)

    class Meta:
        model = PostComments
        fields = ('id', 'user', 'time', 'body')