from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from udhari_user.models import UdhariUser
from udhari_user.serializers import UserSerializer


class UserPermission(BasePermission):
    message = "Only the user themselves can update their profile"

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        if request.method in SAFE_METHODS:
            return True

        return obj.uid == request.user.uid

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class UserViewSet(viewsets.ModelViewSet):

    permission_classes = [UserPermission]
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'head', ]
    queryset = UdhariUser.objects.all()
