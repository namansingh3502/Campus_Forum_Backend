from rest_framework import serializers
from .models import *


class UserProfileSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'username',
            'full_name',
            'department',
            'user_image'
        )

    def get_full_name(self, user):
        return "%s %s %s" % (user.first_name, user.middle_name, user.last_name)
