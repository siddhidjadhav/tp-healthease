from django.contrib import admin
from .models import Insurance, InsuranceDetails, InsurancePurchaseHistory

# Register your models here.

admin.site.register(Insurance)
admin.site.register(InsuranceDetails)
admin.site.register(InsurancePurchaseHistory)
