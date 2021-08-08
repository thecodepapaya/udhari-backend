from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import SAFE_METHODS, BasePermission
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
    permission_classes = [ExpensePermission]
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', ]

    def list(self, request):
        expenses = Expense.objects.filter(user=request.user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # def create(self, request):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # def retrieve(self, request, pk=None):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # def update(self, request, pk=None):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # def partial_update(self, request, pk=None):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # def destroy(self, request, pk=None):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # def get(self, request, format=None):
    #     user = Expense.objects.all()
    #     serializer = ExpenseSerializer(user, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request, format=None):
    #     serializer = ExpenseSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
