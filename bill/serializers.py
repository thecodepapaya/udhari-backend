from rest_framework import serializers

from .models import Bill, BillContributor


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'


class BillContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillContributor
        fields = '__all__'
