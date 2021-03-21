from django.db import models


class User(models.Model):
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, primary_key=True)
    photo_url = models.URLField()
    uid = models.CharField(max_length=30)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.phone_number}'
