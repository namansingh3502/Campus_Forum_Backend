from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from AuthenticationApp.models import UserProfile
from .models import *
from .serializers import *

# Create your views here.

@api_view(['GET'])
def BasicUser(request):
    user = UserProfile.objects.get(pk=1)
    serializer = BasicUserSerializer(user)

    return Response(serializer.data)
