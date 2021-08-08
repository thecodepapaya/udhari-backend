from django.urls import path
from .views import ExpenseViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from expense import views

router = DefaultRouter()
router.register(r'', ExpenseViewSet, basename='expense')
urlpatterns = router.urls
