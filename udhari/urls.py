from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from udhari import views

router = DefaultRouter()
router.register(r'', views.UdhariViewSet, basename='udhari')
urlpatterns = router.urls
