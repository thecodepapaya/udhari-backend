from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import PermissionsMixin, AbstractUser


class UdhariUserManager(BaseUserManager):
    def create_user(self, uid, phone_number, country_code, name, password, **other):

        user = self.model(uid=uid, phone_number=phone_number,
                          country_code=country_code, name=name, **other)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, uid, phone_number, country_code, name, password, **other):

        other.setdefault('is_active', True)
        other.setdefault('is_staff', True)
        other.setdefault('is_superuser', True)

        return self.create_user(uid, phone_number, country_code, name, password, **other)


class UdhariUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=11)
    country_code = models.CharField(max_length=4, default="+91")
    photo_url = models.URLField(default='https://i.stack.imgur.com/l60Hf.png')
    uid = models.CharField(max_length=30, primary_key=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    fcm_token = models.CharField(
        max_length=200, default="", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    REQUIRED_FIELDS = ('phone_number', 'country_code', 'name')
    USERNAME_FIELD = 'uid'

    objects = UdhariUserManager()

    def __str__(self):
        return f'{self.name} {self.phone_number}'
