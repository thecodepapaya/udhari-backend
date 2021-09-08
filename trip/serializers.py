from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Trip, TripMember


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


class TripMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripMember
        fields = '__all__'
