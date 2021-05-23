from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import UniqueConstraint

class UdhariUser(AbstractBaseUser):
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=11)
    country_code = models.CharField(max_length=4, default="+91")
    photo_url = models.URLField(default='https://i.stack.imgur.com/l60Hf.png')
    uid = models.CharField(max_length=30, primary_key=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    fcm_token = models.CharField(
        max_length=200, default="", null=True, blank=True)
    auth_token = models.CharField(max_length=64)
    # is_admin = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)

    # REQUIRED_FIELDS = ('phone_number', 'country_code', 'name')
    # USERNAME_FIELD = 'uid'

    # objects = UdhariUserManager()

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin

    # def has_module_perms(self, app_label):
    #     return True

    def __str__(self):
        return f'{self.name} {self.phone_number}'

# class UdhariUserManager(BaseUserManager):

#     def create_user(self, uid, phone_number, country_code, name, password=None):
#         if not uid:
#             raise ValueError("Must have a UID")
#         if not phone_number:
#             raise ValueError("Must have a phone number")
#         if not country_code:
#             raise ValueError("Phone number must accompany a country code")
#         if not name:
#             raise ValueError("Must have a name")

#         user = self.model(
#             phone_number=phone_number,
#             uid=uid,
#             country_code=country_code,
#             name=name,
#         )

#         user.save(using=self._db)
#         return user

#     def create_superuser(self, uid, phone_number, country_code, name, password):
#         user = self.create_user(
#             uid=uid,
#             phone_number=phone_number,
#             country_code=country_code,
#             name=name,
#             password=password,
#         )

#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True

#         user.save(using=self._db)
#         return user
