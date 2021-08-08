
from copy import deepcopy

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from udhari.models import Udhari
from udhari.serializers import UdhariSerializer


class udhari(APIView):
    def get(self, request, format=None):
        try:
            udhari = Udhari.objects.all()
            serializer = UdhariSerializer(udhari, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Udhari.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
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
            if data1['lender'] == data1['borrower']:
                return Response({'data': 'Lender and borrower cannot be same'}, status=status.HTTP_403_FORBIDDEN)
            if data1['amount'] < 0:
                return Response({'data': 'Amount must be non-negative'}, status=status.HTTP_403_FORBIDDEN)
            if data1['created_by'] != data1['lender'] and data1['created_by'] != data1['borrower']:
                return Response({'data': 'Created_by must be either equal to lender or borrower'}, status=status.HTTP_403_FORBIDDEN)

            serializer1.save()
            serializer2.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)


class edit(APIView):
    def put(self, request, pk, format=None):
        # verify JWT before doing anything else
        jwt_uid = "udiasnasdsa"
        
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        # verify JWT before doing anything else
        jwt_uid = "udiasnasdsa"
        udhari = Udhari.objects.get(pk=pk)
        if udhari.borrower == jwt_uid or udhari.lender == jwt_uid:
            udhari.delete()
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if udhari.created_by == jwt_uid:
            Udhari.objects.get(pk=pk+1).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
