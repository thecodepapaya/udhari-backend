from copy import deepcopy

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from .models import Trip, TripMember
from .serializers import TripMemberSerializer, TripSerializer


class TripPermission(BasePermission):
    message = "Trip can only be viewed or modified by the user who created them"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class TripMemberPermission(BasePermission):
    message = "Trip member can only be modified by the user who created the trip. They can be viewed by all the other members"

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        if request.method in SAFE_METHODS:
            return True
        # Case for edit access by self(for removing oneself from the trip) or by trip creator
        return request.user == Trip.objects.get(pk=obj.belongs_to_trip.id).created_by or request.user == obj.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class TripViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, ExpensePermission]
    # permission_classes = [TripPermission]
    serializer_class = TripSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', ]

    def get_queryset(self):
        # print(f"Received user: {self.request.user}")
        return Trip.objects.all()

    def create(self, request, *args, **kwargs):
        data = deepcopy(request.data)
        data['created_by'] = request.user.uid
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = deepcopy(request.data)
        data['created_by'] = request.user.uid
        data['updated_at'] = timezone.now()
        serializer = self.get_serializer(self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TripMemberViewSet(viewsets.ModelViewSet):
    serializer_class = TripMemberSerializer
    permission_classes = [TripMemberPermission]
    http_method_names = ['get', 'post', 'delete', 'head', ]

    def get_queryset(self, *args, **kwargs):
        if TripMember.objects.filter(belongs_to_trip=self.kwargs['trip_lookup_pk'], user=self.request.user).exists():
            return TripMember.objects.filter(belongs_to_trip=self.kwargs['trip_lookup_pk'])

    def create(self, request, *args, **kwargs):
        data = deepcopy(request.data)
        data['belongs_to_trip'] = self.kwargs['trip_lookup_pk']
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            if TripMember.objects.filter(belongs_to_trip=serializer.validated_data['belongs_to_trip'], user=serializer.validated_data['user']).exists():
                return Response({'detail': 'Member already part of given Trip'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
