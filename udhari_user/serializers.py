from hashlib import sha256

from django.utils.datetime_safe import datetime
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import UdhariUser


# class POSTUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UdhariUser
#         fields = '__all__'

#     def to_internal_value(self, data):
#         data['auth_token'] = sha256(
#             str(datetime.now()).encode('utf-8')).hexdigest()
#         return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdhariUser
        fields = ['uid', 'name',
                   'phone_number', 'country_code', 'photo_url', 'fcm_token']
