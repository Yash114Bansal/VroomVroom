from django.contrib import admin
from accounts.admin import BaseImportExportAdmin
from .models import PassengerPayment

@admin.register(PassengerPayment)
class PassengerPaymentAdmin(BaseImportExportAdmin):
    pass
