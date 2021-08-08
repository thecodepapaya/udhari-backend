from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from udhari_user.models import UdhariUser

admin.site.register(UdhariUser)
