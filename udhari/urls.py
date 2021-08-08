from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from udhari import views

urlpatterns = [
    path('', views.udhari.as_view()),
    path('edit/<pk>', views.edit.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
