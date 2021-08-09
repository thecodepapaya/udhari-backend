from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from bill import views
from rest_framework.routers import DefaultRouter

from .views import BillViewSet

router = DefaultRouter()
router.register(r'', BillViewSet, basename='bill')
urlpatterns = router.urls
