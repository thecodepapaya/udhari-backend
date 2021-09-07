from copy import deepcopy, error
from datetime import date

from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, status, viewsets
from rest_framework import serializers
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from bill.models import Bill, BillContributor
from bill.serializers import BillContributorSerializer, BillSerializer


class BillPermission(BasePermission):
    message = "Bill can only be modified by the bill creator. Bill can be viewed by all associated contributors"

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        # TODO: add missing case - give view permission to people added as contributors to a bill
        # WTF: this was automatically handled by allowing all authenticated user to view the data.
        # List of users who were eligible to see the bills were created by get_queryset().
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.created_by

    def has_permission(self, request, view):
        return super().has_permission(request, view)


class BillContributorPermission(BasePermission):
    message = "Bill contributor can only be modified by the bill contributor or bill creator. Bill contributor can be viewed by all bill contributors"

    # TODO add permissions
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        #TODO add case for viewable only to other contributors of the bill
        if request.method in SAFE_METHODS:
            return True
        # Case for edit access by self and bill creator
        return request.user == Bill.objects.get(pk=obj.belongs_to_bill.id).created_by or request.user == obj.user

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

    def create(self, request, *args, **kwargs):
        data = deepcopy(request.data)
        data['created_by'] = request.user.uid
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            contributor = BillContributor.objects.create(
                user=request.user, belongs_to_bill=Bill.objects.get(pk=serializer.data['id']))
            # contribution_serializer = BillContributorSerializer(
            #     data=contributor)
            contributor.save()
            # if contribution_serializer.is_valid():
            #     contribution_serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            # else:
            #     print("invalid bill contributor")
            #     return Response(contribution_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            print("invalid bill")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = deepcopy(request.data)
        data['created_by'] = request.user.uid
        data['updated_at'] = timezone.now()
        serializer = self.get_serializer(self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BillContributorViewSet(viewsets.ModelViewSet):
    serializer_class = BillContributorSerializer
    permission_classes = [BillContributorPermission]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', ]
    queryset = BillContributor.objects.all()

    def get_queryset(self, *args, **kwargs):
        return BillContributor.objects.filter(belongs_to_bill=self.kwargs['bill_lookup_pk'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            bill_creator = Bill.objects.get(
                pk=serializer.validated_data['belongs_to_bill'].id).created_by
            if bill_creator != request.user:
                return Response({'detail': 'Only the bill creator is allowed to add contributors'}, status=status.HTTP_401_UNAUTHORIZED)

            
            if BillContributor.objects.filter(belongs_to_bill=serializer.validated_data['belongs_to_bill'], user=serializer.validated_data['user']).exists():
                return Response({'detail': 'Cannot add duplicate entry for user in the same bill'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = deepcopy(request.data)
        data['updated_at'] = timezone.now()
        data['belongs_to_bill'] = self.kwargs['bill_lookup_pk']
        data['user'] = self.kwargs['bill_lookup_pk']
        serializer = self.get_serializer(self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
