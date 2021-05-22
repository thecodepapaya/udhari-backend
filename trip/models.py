from django.db import models
from udhari_user.models import UdhariUser


class Trip(models.Model):
    name = models.CharField(max_length=30, default='New Trip')
    notes = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        UdhariUser, on_delete=models.CASCADE, related_name='trip_creator')
    total_amount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.name} at {self.created_at} by {self.created_by}'
