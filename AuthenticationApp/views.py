from django.core.files.storage import default_storage
from django.http.response import HttpResponse
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .models import *

import uuid

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):

    user = UserProfile.objects.get(pk=request.user.pk)
    serializer = UserProfileSerializer(user)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, username):

    try:
        user = UserProfile.objects.get(username=username)
        serializers = UserProfileSerializer(user)
        return Response(serializers.data)
    except UserProfile.DoesNotExist:
        return Response({'message':'User does not exist.'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_image(request):
    user = UserProfile.objects.get(pk=request.user.pk)

    for file in request.FILES:
        file = request.FILES[file]
        file_extension = file.name.split('.')[-1]
        file.name = str(user.username) + '.' + file_extension + "-" + str(uuid.uuid4())

        default_storage.delete("profile_pic/%s" % file.name)
        default_storage.save("profile_pic/%s" % file.name, file)

        user.user_image = "profile_pic/" + file.name
        user.save()

    serializer = UserProfileSerializer(user)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def csrf_token_generator(request):
    csrf_token = get_token(request)

    return HttpResponse(csrf_token)