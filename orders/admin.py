from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.UserCheckout)
admin.site.register(models.UserAddress)
admin.site.register(models.Order)