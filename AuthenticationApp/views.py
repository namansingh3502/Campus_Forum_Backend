import os

from coreapi.compat import force_text
from django.http.response import HttpResponse
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import EmailMessage
from Campus_Forum.custom_storage import MediaStorage

from .serializers import *
from .models import *
from .forms import RegistrationForm, PasswordResetForm
import uuid

from .tokens import account_activation_token


@api_view(['POST'])
def user_registration(request):
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

        mail_subject = 'Account activation link.'
        message = render_to_string('acc_activate_email.html', {
            'user': user,
            'domain': "https://college-forum.vercel.app",
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
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({'message': 'User does not exist.'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_image(request):
    user = UserProfile.objects.get(pk=request.user.pk)

    # file directory in bucket
    file_directory = 'profile_pic/{username}'.format(username=user)

    for file in request.FILES:
        file_obj = request.FILES[file]
        file_extension = file_obj.name.split('.')[-1]

        file_name = "%s_%s.%s" % (
            user.username,
            uuid.uuid4(),
            file_extension
        )

        # full file path inside the bucket
        # full path structure : profile_pic/<username>/<username>_<rand_value>.extension

        file_path = os.path.join(
            file_directory,
            file_name
        )

        # save file in s3 bucket and url
        media_storage = MediaStorage()

        # update image url in db
        media_storage.save(file_path, file_obj)
        user.user_image = media_storage.url(file_path)
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


@api_view(['POST'])
def email_reset_link(request):
    email = request.data['data']['email']
    try:
        user = UserProfile.objects.get(email=email)
        mail_subject = 'Password reset link.'
        message = render_to_string('reset_password_email.html', {
            'user': user,
            'domain': 'https://college-forum.vercel.app',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email = EmailMessage(
            mail_subject, message, to=[email]
        )
        email.send()
        return Response({'msg': 'Password link sent successfully.'}, status=200)
    except UserProfile.DoesNotExist:
        return Response({'msg': 'No user exists with given email.'}, status=400)


@api_view(['POST'])
def reset_password(request):
    password = request.data['data']
    uidb64 = request.data['uidb64']
    token = request.data['token']

    form = PasswordResetForm(password)

    if form.is_valid():
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserProfile.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return Response({'msg': "Password updated successfully."}, status=200)
        else:
            return Response({'msg': "Password update link is invalid!."}, status=400)
    else:
        return Response({'msg': form.error_messages}, status=400)
