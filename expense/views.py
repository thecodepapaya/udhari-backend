from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from expense.models import Expense
from expense.serializers import ExpenseSerializer


class ExpensePermission(BasePermission):
    message = "Expenses can only be viewed or modified by the user who created them"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class ExpenseViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, ExpensePermission]
    permission_classes = [ExpensePermission]
    serializer_class = ExpenseSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', ]

    def get_queryset(self):
        print(f"Received user: {self.request.user}")
        return Expense.objects.filter(user=self.request.user)

    # TODO Override create method to verify request.user == request.data.user. Otherwise anyone would be able to create expense with anybody's uid.
