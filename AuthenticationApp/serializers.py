from rest_framework import serializers
from .models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'username',
            'prefix',
            'first_name',
            'middle_name',
            'last_name',
            'department',
            'user_image'
        )
