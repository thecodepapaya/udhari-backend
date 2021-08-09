
from copy import deepcopy

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from udhari.models import Udhari
from udhari.serializers import UdhariSerializer


class UdhariPermission(BasePermission):
    message = "Udhari can only be viewed or modified by the user associated with it"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.visible_to

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class UdhariViewSet(viewsets.ModelViewSet):

    serializer_class = UdhariSerializer
    permission_classes = [UdhariPermission]
    # permission_classes = [UdhariPermission, IsAuthenticated]

    def get_queryset(self):
        # print(f"Received user: {self.request.user}")
        return Udhari.objects.filter(visible_to=self.request.user)

    def create(self, request, *args, **kwargs):
        udhari1 = deepcopy(request.data)
        udhari2 = deepcopy(request.data)
        udhari1['visible_to'] = udhari2['borrower']
        udhari2['visible_to'] = udhari2['lender']
        serializer1 = UdhariSerializer(data=udhari1)
        serializer2 = UdhariSerializer(data=udhari2)
        if serializer1.is_valid() and serializer2.is_valid():
            data1 = serializer1.validated_data

            # created_by ID must match with JWT UID
            # created_by must be same as borrower or lender
            # borrower and lender must not be same
            # amount not negative
            if data1['created_by'] != request.user:
                return Response({'detail': 'Udhari can only be created in the name of logged in user.'}, status=status.HTTP_401_UNAUTHORIZED)
            if data1['lender'] == data1['borrower']:
                return Response({'detail': 'Lender and borrower cannot be same'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            if data1['amount'] < 0:
                return Response({'detail': 'Amount must be non-negative'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            if data1['created_by'] != data1['lender'] and data1['created_by'] != data1['borrower']:
                return Response({'detail': 'created_by must be either equal to lender or borrower'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            serializer1.save()
            serializer2.save()
            return Response(serializer1.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        self.perform_destroy(instance)

        if request.user == self.get_object().created_by:
            print("Delete two")
            try:
                pair_instance_id = instance_id - 1 if instance_id % 2 == 0 else instance_id + 1
                pair_instance = Udhari.objects.get(pk=pair_instance_id)
                self.perform_destroy(pair_instance)
            except Udhari.DoesNotExist:
                print("Maybe already deleted")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        data = request.data.copy()
        # Handle changes to visible_to and created_by. visible_to and created_by must not be edited directly
        data['visible_to'] = instance.visible_to_id
        data['created_by'] = instance.created_by_id

        if data['lender'] == data['borrower']:
            return Response({'detail': 'Lender and borrower cannot be same'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if float(data['amount']) < 0:
            return Response({'detail': 'Amount must be non-negative'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if data['created_by'] != data['lender'] and data['created_by'] != data['borrower']:
            return Response({'detail': 'created_by must be either equal to lender or borrower'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # visible_to must be changed if corresponding lender/borrower is replaced with new user
        if instance_id % 2 == 1:
            data['visible_to'] = data['borrower']
        else:
            data['visible_to'] = data['lender']

        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if request.user == self.get_object().created_by:
            print("Update two")
            try:
                pair_instance_id = instance_id - 1 if instance_id % 2 == 0 else instance_id + 1
                pair_instance = Udhari.objects.get(pk=pair_instance_id)

                if pair_instance_id % 2 == 1:
                    data['visible_to'] = data['borrower']
                else:
                    data['visible_to'] = data['lender']

                serializer2 = self.get_serializer(pair_instance, data=data)
                serializer2.is_valid(raise_exception=True)
                self.perform_update(serializer2)
            except Udhari.DoesNotExist:
                print("Maybe already deleted")

        return Response(serializer.data, status=status.HTTP_200_OK)
