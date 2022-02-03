from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile
from .serializers import *

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):

    user = UserProfile.objects.get(pk=request.user.pk)
    serializer = UserProfileSerializer(user)

    return Response(serializer.data)
