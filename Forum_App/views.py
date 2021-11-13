from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from AuthenticationApp.models import UserProfile
from .models import *
from .serializers import *

@api_view(['GET'])
def ChannelList(request):

    channels = ChannelDetail.objects.all()
    serializer = ChannelListSerializer(channels, many=True)

    return Response(serializer.data)

class Posts(APIView):

    def get(self,request):

        posts = PostDetail.objects.all()
        serializer = PostDetailSerializer(posts, many=True)

        return Response(serializer.data)

    def post(self,request):

        print(request)

        return Response("post received")

@api_view(['GET'])
def PostCommentList(request, post_id):

    comments = PostComment.objects.filter(post=post_id)
    serializer = PostCommentSerializer(comments,many=True)

    return Response(serializer.data)

@api_view(['GET'])
def PostLikeList(request, post_id):

    likes = PostLike.objects.filter(post=post_id)
    serializers = PostLikesSerializer(likes,many=True)

    return Response(serializers.data)
