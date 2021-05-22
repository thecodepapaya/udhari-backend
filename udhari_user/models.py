from django.db import models
from django.db.models import UniqueConstraint


class UdhariUser(models.Model):
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=11)
    country_code = models.CharField(max_length=4, default="+91")
    photo_url = models.URLField()
    uid = models.CharField(max_length=30, primary_key=True)
    joined_on = models.DateTimeField(auto_now_add=True)
    fcm_token = models.CharField(
        max_length=200, default="", null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.phone_number}'
