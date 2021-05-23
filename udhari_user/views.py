from django.shortcuts import render
from rest_framework.views import APIView

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from udhari_user.models import UdhariUser
from udhari_user.serializers import UdhariUserSerializer


class user(APIView):
    def get(self, request, pk, format=None):
        try:
            user = UdhariUser.objects.get(pk=pk)
            serializer = UdhariUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UdhariUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class register(APIView):
    def post(self, request, format=None):
        serializer = UdhariUserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(request.data)
            print(serializer.validated_data)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        print(serializer)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # TODO: remove later
    def get(self, request, format=None):
        users = UdhariUser.objects.all()
        serializer = UdhariUserSerializer(users, many=True)
        return Response(serializer.data)
