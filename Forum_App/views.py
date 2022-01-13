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

    posts = Post.objects.filter(posted_in__in=channel_list, is_hidden=False).distinct()[:5]
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


@api_view(['GET'])
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
    newPost = NewPost(data)
    msg="dont know what happened"
    if newPost.is_valid():
        post = Post(body=data['body'], media_count=data['media_count'])
        post.save()
        msg = "post created successfully"
    else:
        msg = "some error occured while creating post"

    return Response({'msg':msg})