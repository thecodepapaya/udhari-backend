from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from expense import views

urlpatterns = [
    path('expense/', views.expense.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
