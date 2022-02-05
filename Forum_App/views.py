from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import json

from AuthenticationApp.models import *
from .models import *
from .serializers import *
from .forms import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def channels(request):

    channel_list = UserProfile.objects.get(pk=request.user.pk).member_of.filter(is_active=True)
    serializer = ChannelListSerializer(channel_list, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def posts_user(request):

    channel = list(UserProfile.objects.get(pk=request.user.pk).member_of.all().values_list('id'))
    channel_list = list(map(lambda x: x[0], channel))

    posts = Post.objects.filter(posted_in__in=channel_list, is_hidden=False).distinct()[:10]
    post_id = list(posts.values_list('id'))
    post_id = list(map(lambda x: x[0], post_id))

    data = User_Post_Media.objects.filter(post__in=post_id).order_by('-pk')

    serializer = PostSerializer(data, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_comment(request, post_id):

    comments = Post_Comment.objects.filter(post=post_id).order_by('pk')
    serializer = CommentSerializer(comments, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_likes(request, post_id):

    likes = Post_Like.objects.filter(post=post_id)
    serializer = LikeSerializer(likes, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def channel_details(request, channel_id):

    try:
        data = Channel.objects.get(id=channel_id)
    except Channel.DoesNotExist:
        return Response({'msg':'Channel does not exist'}, status=400)

    serializer = ChannelDetailsSerializer(data)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def channel_post(request, channel_id):

    channel = Channel.objects.get(id=channel_id)
    member_of = UserProfile.objects.get(id=request.user.pk).member_of.all()

    if channel not in member_of:
        return Response({'msg':'Not a member of channel'}, status=400)

    if( not channel.is_active ):
        return Response({'msg':'Channel not active'}, status=400)

    posts = Post.objects.filter(posted_in=channel_id, is_hidden=False).distinct()[:10]
    post_id = list(posts.values_list('id'))
    post_id = list(map(lambda x: x[0], post_id))

    data = User_Post_Media.objects.filter(post__in=post_id).order_by('-pk')
    serializer = PostSerializer(data, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_post_like(request, post_id):

    try:
        like = Post_Like.objects.get(
            user_id=request.user.pk,
            post_id=post_id
        )
        like.delete()
    except Post_Like.DoesNotExist:
        like = Post_Like(
            user_id=request.user.pk,
            post_id=post_id
        )
        like.save()

    return Response({'msg':'got the call'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_post(request):
    data = json.loads(request.body)

    if data['channel_list'] == []:
        return Response(status=400)

    postForm = PostForm(data)

    if postForm.is_valid():
        post = Post.objects.create(
            body = data['body'],
            media_count = data['media_count']
        )
        post.save()
        for channel in data['channel_list']:
            try:
                channel = Channel.objects.get(id=channel['id'])
                post.posted_in.add(channel)
            except Channel.DoesNotExist:
                return Response(status=400)

        userPostMedia = User_Post_Media.objects.create(
            user_id=request.user.pk,
            post_id=post.pk
        )
    else:
        return Response(status=400)
    data = User_Post_Media.objects.get(post_id=post)
    serializer = PostSerializer(data)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_comment(request):

    data = json.loads(request.body)

    try:
        post = Post.objects.get(id=data['post'])
        commentForm = CommentForm(data)

        if commentForm.is_valid():
            comment = Post_Comment.objects.create(
                user_id=request.user.pk,
                post_id=data['post'],
                body=data['body']
            )
            comment.save()
        else:
            return Response(status=400)
    except Post.DoesNotExist:
        return Response(status=400)

    comments = Post_Comment.objects.get(id=comment.pk)
    serializer = CommentSerializer(comments)

    return Response(serializer.data)