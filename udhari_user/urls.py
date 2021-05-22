from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from udhari_user import views

urlpatterns = [
    path('user/<pk>', views.user.as_view()),
    path('register/', views.register.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
