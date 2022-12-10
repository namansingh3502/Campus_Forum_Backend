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
from rest_framework import status


from Campus_Forum.custom_storage import MediaStorage
from .serializers import *
from .models import *
from .forms import RegistrationForm, PasswordResetForm
import uuid

from .tokens import account_activation_token


@api_view(['POST'])
def user_registration(request):
    """
    User registration api
    if user is already signed in and tries to register then return with HTTP_400_BAD_REQUEST
    User Registration form data is validated then generate activation token
    send token to email provided by the user.
    if form_has errors return error with HTTP_400_BAD_REQUEST
    """

    # TODO : Handle send_email() failure. Nothing happens if email in send_mail() fails

    user = request.user
    if user.is_authenticated:
        return HttpResponse({'Message': "You are already authenticated."}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data['data']

    data['gender'] = data['gender']['value']
    data['department'] = data['department']['value']

    form = RegistrationForm(data)

    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        mail_subject = 'Forum Account activation link.'
        message = render_to_string('account_activate_email.html', {
            'user': user,
            'domain': os.environ.get("FRONTEND_SERVER_ADDRESS"),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject,
            message,
            to=[to_email]
        )
        email.send()

    else:
        return Response({'msg': form.errors.values()}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'msg': "User Registration Successful."}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    returns user_profile for currently logged-in user
    """
    user = UserProfile.objects.get(pk=request.user.pk)
    serializer = UserProfileSerializer(user)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, username):

    """
    returns user_profile of the given username
    returns 404 if user doesn't exist
    """

    try:
        user = UserProfile.objects.get(username=username)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)


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

    # TODO: Figure out use of api
    """
    don't remember why it was created
    returns csrf token
    """

    csrf_token = get_token(request)
    return HttpResponse(csrf_token)


@api_view(['GET'])
def activate_user(request, uidb64, token):

    """
    validates activation token sent via email
    if activation token is validated activate use account else return 400
    """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserProfile.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'msg': "Account activated."}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': "Activation link is invalid!."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def email_reset_link(request):

    """
    generate password reset token for account linked to the user_email
    send password reset link to the user_email
    If user_email not linked to account return HTTP_400_BAD_REQUEST
    """

    # TODO : Handle send_email() failure. Nothing happens if email in send_mail() fails

    user_email = request.data['data']['email']
    try:
        user = UserProfile.objects.get(email=user_email)
        mail_subject = 'Password reset link.'
        message = render_to_string('reset_password_email.html', {
            'user': user,
            'domain': os.environ.get("FRONTEND_SERVER_ADDRESS"),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email = EmailMessage(
            mail_subject, message, to=[user_email]
        )
        email.send()
        return Response({'msg': 'Password link sent successfully.'}, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({'msg': 'No user exists with given email.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_password(request):

    """
    validate password reset token and password
    if password validates reset password and send success mail to user email
    if password validations fails return HTTP_400_BAD_REQUEST
    """

    # TODO : Handle send_email() failure. Nothing happens if email in send_mail() fails

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

            user_email = user.email
            mail_subject = 'Password reset successful.'
            message = render_to_string('reset_password_success.html', {
                'user': user,
                'domain': os.environ.get("FRONTEND_SERVER_ADDRESS")
            })
            email = EmailMessage(
                mail_subject, message, to=[user_email]
            )
            email.send()
            return Response({'msg': "Password updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': "Password reset link is invalid!."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'msg': form.error_messages}, status=status.HTTP_400_BAD_REQUEST)
