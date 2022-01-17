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
def channels(request):
    """
        Returns the list of channels the user is member of.
        path:  http://127.0.0.1:8000/forum/channel-list
    """
    channel_list = UserProfile.objects.get(pk=request.user.pk).member_of.filter(is_active=True)
    serializer = ChannelListSerializer(channel_list, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def posts_user(request):

    channel = list(UserProfile.objects.get(pk=request.user.pk).member_of.all().values_list('id'))
    channel_list = list(map(lambda x: x[0], channel))

    posts = Post.objects.filter(posted_in__in=channel_list, is_hidden=False).distinct()
    post_id = list(posts.values_list('id'))
    post_id = list(map(lambda x: x[0], post_id))

    data = User_Post_Media.objects.filter(post__in=post_id).order_by('-pk')

    serializer = PostSerializer(data, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def post_comment(request, post_id):

    comments = Post_Comment.objects.filter(post=post_id)
    serializer = CommentSerializer(comments, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def post_likes(request, post_id):

    likes = Post_Like.objects.filter(post=post_id)
    serializer = LikeSerializer(likes, many=True)

    return Response(serializer.data)


@api_view(['POST'])
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
def new_post(request):
    data = json.loads(request.body)

    if data['text'] == "" and data['channel_list'] == []:
        return Response(status=400)

    newPost = NewPost(data)

    if newPost.is_valid() :
        post = Post.objects.create(
            body = data['text'],
            media_count = data['media_count']
        )
        post.save()
        for channel in data['channel_list']:
            try:
                channel = Channel.objects.get(id=channel['id'])
                post.posted_in.add(channel)
            except Channel.DoesNotExist:
                msg = "Error with channel id"
                return Response(status=400)

        userPostMedia = User_Post_Media.objects.create(
            user_id=request.user.pk,
            post_id=post.pk
        )
    else:
        return Response(status=400)

    return Response({'msg':'post created succesfully'})