from django.http import Http404, HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated)
from rest_framework.response import Response

from bill.models import Bill, BillContributor
from bill.serializers import BillContributorSerializer, BillSerializer

from datetime import date
from dateutil.relativedelta import relativedelta


class BillPermission(BasePermission):
    message = "Bill can only be viewed or modified by the bill contributors"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class BillContributorPermission(BasePermission):
    message = "Bill contributor can only be modified by the bill contributor or bill creator. Bill contributor can be viewed by all bill contributors"

    # TODO add permissions
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class BillViewSet(viewsets.ModelViewSet):
    serializer_class = BillSerializer
    permission_classes = [BillPermission]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', ]

    def get_queryset(self):
        # print(f"Received user: {self.request.user}")
        contributions = list(BillContributor.objects.filter(user=self.request.user).filter(
            created_at__gte=date.today() + relativedelta(months=-6)).values('belongs_to_bill').iterator())
        ids = []
        for c in contributions:
            ids.append(c['belongs_to_bill'])
        return Bill.objects.filter(id__in=ids)


class BillContributorViewSet(viewsets.ModelViewSet):
    serializer_class = BillContributorSerializer
    # permission_classes = [BillPermission]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', ]
    queryset = BillContributor.objects.all()
