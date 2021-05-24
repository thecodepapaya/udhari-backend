
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
    def get(self, request, pk, format=None):
        try:
            # udhari = Udhari.objects.get(pk=pk)
            # serializer = UdhariSerializer(udhari)
            udhari = Udhari.objects.all()
            serializer = UdhariSerializer(udhari, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Udhari.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk, format=None):
        serializer = UdhariSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # created_by ID must match with JWT UID
            # created_by must be same as borrower or lender
            # borrower and lender must not be same
            # amount not negative
            if data['lender'] == data['borrower']:
                return Response({'data': 'Lender and borrower cannot be same'}, status=status.HTTP_403_FORBIDDEN)
            if data['amount'] <= 0:
                return Response({'data': 'Amount cannot be negative'}, status=status.HTTP_403_FORBIDDEN)
            if data['created_by'] != data['lender'] and data['created_by'] != data['borrower']:
                return Response({'data': 'Created_by must be either equal to lender or borrower'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class merge(APIView):
#     def post(self,request,format=None):
