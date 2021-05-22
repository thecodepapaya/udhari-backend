from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import UdhariUser


class UdhariUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdhariUser
        fields = ['name', 'phone_number', 'country_code',
                  'photo_url', 'uid', 'joined_on', 'fcm_token']
