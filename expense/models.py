from django.db import models
from udhari_user.models import UdhariUser


class Expense(models.Model):
    notes = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    user = models.ForeignKey(UdhariUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.amount} by {self.user} at {self.created_at}'
