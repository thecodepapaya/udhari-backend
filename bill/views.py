from django.http import Http404, HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated)
from rest_framework.response import Response

from bill.models import Bill, BillContributor
from bill.serializers import BillContributorSerializer, BillSerializer


class BillPermission(BasePermission):
    message = "Bill can only be viewed or modified by the bill contributors"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class BillViewSet(viewsets.ModelViewSet):
    serializer_class = BillSerializer
    # permission_classes = [BillPermission]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', ]
    queryset = Bill.objects.all()
