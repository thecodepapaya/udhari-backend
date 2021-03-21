from django.contrib.postgres.fields import ArrayField
from django.db import models
from user.models import User


class BillContributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    amount_contributed = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.user} share: {self.share} contributed: {self.amount_contributed}'


class Bill(models.Model):
    name = models.CharField(max_length=30, default='New Bill')
    total_amount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)
    notes = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bill_creator')
    # Consists of IDs of BillContributors for this Bill. This would need to be validated upon addition
    contributors_id_array = ArrayField(models.IntegerField(), default=list)

    def __str__(self):
        return f'{self.name} at {self.created_at} by {self.created_by}'
