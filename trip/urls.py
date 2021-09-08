from django.urls import path
from django.urls.conf import include
from expense import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_nested import routers

from .views import TripMemberViewSet, TripViewSet

router = routers.SimpleRouter()
router.register(r'', TripViewSet, basename='trip')
trip_member_router = routers.NestedSimpleRouter(
    router, r'', lookup="trip_lookup")
trip_member_router.register(
    r'member', TripMemberViewSet, basename="trip-member")


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(trip_member_router.urls))
]
