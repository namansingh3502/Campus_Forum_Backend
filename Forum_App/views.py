from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from AuthenticationApp.models import UserProfile
from .models import *
from .serializers import *

class Posts(APIView):

    def get(self,request):

        posts = PostDetail.objects.filter(is_active=True)
        serializer = PostDetailSerializer(posts)

        return Response(serializer.data)

    def post(self,request):

        print(request)

        return Response("post received")

@api_view(['GET'])
def channel_list(request):

    channels = ChannelDetail.objects.all()
    serializer = ChannelListSerializer(channels)

    return Response(serializer.data)
