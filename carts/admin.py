from django.contrib import admin
from . import models

class CartItemInline(admin.TabularInline):
    model = models.CartItem


class CartAdmin(admin.ModelAdmin):
    inlines = (CartItemInline,)
    class Meta:
        model = models.Cart


admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartItem)
