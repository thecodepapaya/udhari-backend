from django.contrib import admin
from bill.models import Bill, BillContributor

admin.site.register(Bill)
admin.site.register(BillContributor)