from hashlib import sha256

from django.utils.datetime_safe import datetime
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Udhari


class UdhariSerializer(serializers.ModelSerializer):
    class Meta:
        model = Udhari
        fields = '__all__'

    def to_internal_value(self, data):
        return super().to_internal_value(data)
