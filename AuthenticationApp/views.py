from django.core.files.storage import default_storage
from django.http.response import HttpResponse
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .models import *
from firebaseConfig import storage as firebaseStorage


# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):

    user = UserProfile.objects.get(pk=request.user.pk)
    serializer = UserProfileSerializer(user)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_image(request):
    user = UserProfile.objects.get(pk=request.user.pk)

    for file in request.FILES:
        file = request.FILES[file]
        file_extension = file.name.split('.')[-1]
        file.name = str(user.pk) + '.' + file_extension

        try:
            default_storage.save("userImage/" + file.name, file)

            firebaseStorage.child(
                "userImage/" + file.name
            ).put(
                "media/" + "userImage/" + file.name
            )

            fileURL = firebaseStorage.child(
                "userImage/" + file.name
            ).get_url(
                token="9bb2e73f-6b9a-42a1-bef9-78e1794c2a3f"
            )

            user.user_image = fileURL
            user.save()

            default_storage.delete("userImage/" + file.name)

        except Exception as e:
            return Response({"msg": "some error occured."}, status=500)

    serializer = UserProfileSerializer(user)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def csrf_token_generator(request):
    csrf_token = get_token(request)

    return HttpResponse(csrf_token)