from hashlib import sha256

from django.utils.datetime_safe import datetime
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import UdhariUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdhariUser
        fields = ['uid', 'name',
                  'phone_number', 'country_code', 'photo_url', 'fcm_token']
