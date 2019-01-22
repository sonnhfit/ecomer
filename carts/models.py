from django.db import models
from django.conf import settings
from products import models as product_models
# Create your models here.


class CartItem(models.Model):
    """Cart item"""
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    item = models.ForeignKey(product_models.Variation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return self.item.title

    @property
    def item_name(self):
        return self.item.get_title()

    def remove(self):
        return self.item.remove_from_cart()

    @property
    def item_total(self):
        return self.item.get_price() * self.quantity


class Cart(models.Model):
    """ giỏ hàng
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None, on_delete=models.CASCADE)
    items = models.ManyToManyField(product_models.Variation, through=CartItem)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.id)

    @property
    def count(self):
        return self.cartitem_set.count()

    @property
    def cart_price(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.item_total
        return total

    @property
    def total_count(self):
        cart_count = 0
        for item in self.cartitem_set.all():
            cart_count += item.quantity
        return cart_count