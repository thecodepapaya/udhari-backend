from django.db import models
from user.models import User
from django.contrib.postgres.fields.array import ArrayField


class Trip(models.Model):
    name = models.CharField(max_length=30, default='New Trip')
    notes = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='trip_creator')

    # Consists of IDs of Bills for this Trip
    bills_id_array = ArrayField(models.IntegerField(), default=list)

    def __str__(self):
        return f'{self.name} at {self.created_at} by {self.created_by}'
