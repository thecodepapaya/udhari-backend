from django.utils import timezone
from django.db import models
from trip.models import Trip
from udhari_user.models import UdhariUser


class Bill(models.Model):
    name = models.CharField(max_length=30, default='New Bill')
    total_amount = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00)
    notes = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        UdhariUser, on_delete=models.CASCADE, related_name='bill_creator')
    belongs_to_trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name} at {self.created_at} by {self.created_by}'


class BillContributor(models.Model):
    user = models.ForeignKey(UdhariUser, on_delete=models.CASCADE)
    share = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    amount_contributed = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00)
    belongs_to_bill = models.ForeignKey(
        Bill, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['user',]),
    #         models.Index(fields=['belongs_to_bill',]),
    #     ]

    def __str__(self):
        return f'{self.user} share: {self.share} contributed: {self.amount_contributed}'
