from coreapi.compat import force_text
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import default_storage
from django.http.response import HttpResponse
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import EmailMessage

from .serializers import *
from .models import *
from .forms import RegistrationForm
import uuid

from .tokens import account_activation_token


@api_view(['POST'])
def user_registraion(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated.")

    data = request.data['data']

    data['gender'] = data['gender']['value']
    data['department'] = data['department']['value']

    form = RegistrationForm(data)

    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        mail_subject = 'Activate your forum account.'
        message = render_to_string('acc_activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

    else:
        return Response({'msg': form.errors.values()}, status=500)

    return Response({'msg': "User Registered."}, status=201)


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


@api_view(['GET'])
def activate_user(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserProfile.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'msg': "Account activated."}, status=200)
    else:
        return Response({'msg': "Activation link is invalid!."}, status=400)
