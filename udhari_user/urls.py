from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from udhari_user import views
from udhari_user.views import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
urlpatterns = router.urls
