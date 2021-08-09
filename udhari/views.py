
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
        print(f"Received user: {self.request.user}")
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
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        data = UdhariSerializer(data=request.data)
        if request.user == data['created_by']:
            print("Delete two")
        else:
            print("delete one")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        self.partial_update(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

# class edit(APIView):
#     def put(self, request, pk, format=None):
#         # verify JWT before doing anything else
#         jwt_uid = "udiasnasdsa"

#         return Response(status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, pk, format=None):
#         # verify JWT before doing anything else
#         jwt_uid = "udiasnasdsa"
#         udhari = Udhari.objects.get(pk=pk)
#         if udhari.borrower == jwt_uid or udhari.lender == jwt_uid:
#             udhari.delete()
#         else:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         if udhari.created_by == jwt_uid:
#             Udhari.objects.get(pk=pk+1).delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
