from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from AuthenticationApp.models import *
from .models import *
from .serializers import *


@api_view(['GET'])
def channels(request):
    """
        Returns the list of channels the user is member of.
        path:  http://127.0.0.1:8000/forum/channel-list
    """
    channel_list = UserProfile.objects.get(pk=request.user.pk).member_of.filter(is_active=True)
    serializer = ChannelListSerializer(channel_list, many=True)

    return Response(serializer.data)


class Posts(APIView):

    def get(self, request):

        channel = list(UserProfile.objects.get(pk=request.user.pk).member_of.all().values_list('id'))
        channel_list = list(map(lambda x: x[0], channel))

        posts = Post.objects.filter(posted_in__in=channel_list, is_hidden=False).order_by('-pk').distinct()[:5]
        post_id = list(posts.values_list('id'))
        post_id = list(map(lambda x: x[0], post_id))

        data = User_Post_Media.objects.filter(post__in=post_id)

        serializer = PostSerializer(data, many=True)

        return Response(serializer.data)

    def post(self, request):

        print(request)

        return Response("post received")


@api_view(['GET'])
def post_comment(request, post_id):

    comments = Post_Comment.objects.filter(post=post_id)
    serializer = CommentSerializer(comments, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def post_like(request, post_id):

    likes = Post_Like.objects.filter(post=post_id)
    serializer = LikeSerializer(likes, many=True)

    return Response(serializer.data)


"""
val = list(UserProfile.objects.get(pk=1).member_of.all().values_list('id'))
channel = list(map(lambda x: x[0], val))

posts = Post.objects.filter(posted_in__in=channel, is_hidden=False).order_by('-pk').distinct()[:5]
post_id = list(posts.values_list('id'))
post_id = list(map(lambda x: x[0], post_id))

data = User_Post_Media.objects.filter(post__in=post_id)
data = val.values_list('user__username','post__body')

"""