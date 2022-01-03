from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from AuthenticationApp.models import *
from .models import *
from .serializers import *


@api_view(['GET'])
def channels(request):

    channel_list = UserProfile.objects.get(pk=request.user).member_of.all()
    serializer = ChannelListSerializer(channel_list, many=True)

    return Response(serializer.data)


class Posts(APIView):

    def get(self, request):

        posts = Post.objects.filter(is_hidden=False)
        serializer = PostSerializer(posts, many=True)

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