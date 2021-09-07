from django.urls import path
from django.urls.conf import include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_nested import routers

from bill import views
from rest_framework.routers import DefaultRouter

from .views import BillViewSet, BillContributorViewSet

router = routers.SimpleRouter()
router.register(r'', BillViewSet, basename='bill')
bill_contributor_router = routers.NestedSimpleRouter(router,r'',lookup="bill_lookup")
bill_contributor_router.register(r'contributor',BillContributorViewSet, basename="bill-contributor")

urlpatterns = [
    path(r'',include(router.urls)),
    path(r'',include(bill_contributor_router.urls))
]
