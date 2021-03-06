from django.db import models
from udhari_user.models import UdhariUser


class Udhari(models.Model):
    notes = models.CharField(max_length=200, blank=True, default="")
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    borrower = models.ForeignKey(
        UdhariUser, on_delete=models.CASCADE, related_name='udhari_borrower')
    lender = models.ForeignKey(
        UdhariUser, on_delete=models.CASCADE, related_name='udhari_sender')
    created_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)
    is_merged = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        UdhariUser, on_delete=models.CASCADE, related_name='udhari_creator')
    visible_to = models.ForeignKey(
        UdhariUser, on_delete=models.CASCADE, related_name='udhari_visible_to')

    def __str__(self):
        return f'{self.id} - {self.amount} by {self.created_by}'
