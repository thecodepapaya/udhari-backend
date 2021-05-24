from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from udhari import views

urlpatterns = [
    path('udhari/<pk>', views.udhari.as_view()),
    # path('merge/', views.merge.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
