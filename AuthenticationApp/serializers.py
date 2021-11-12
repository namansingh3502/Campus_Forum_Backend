from rest_framework import serializers
from .models import *

class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=('prefix','first_name','middle_name','last_name','user_image')
