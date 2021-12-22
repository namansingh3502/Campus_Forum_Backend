# from rest_framework import serializers
# from .models import *
#
# class PostDetailSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user', read_only=True)
#     id = serializers.CharField(source='pk', read_only=True)
#
#     class Meta:
#         model=PostDetail
#         fields=['id','username','time','body','image_count']
#
#
# class PostCommentSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user', read_only=True)
#
#     class Meta:
#         model=PostComment
#         fields=('post','username','datetime', 'body')
#
# class PostLikesSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user', read_only=True)
#
#     class Meta:
#         model=PostLike
#         fields=('username',)
#
# class ChannelListSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model=ChannelDetail
#         fields=('channel_name',)
