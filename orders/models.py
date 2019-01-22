from django.db import models
from django.conf import settings
from carts.models import Cart
# Create your models here.


class UserCheckout(models.Model):
    """user thanh toán """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True, default=None, on_delete=models.CASCADE)
    email = models.EmailField('email of guest user', null=True, blank=True)

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.user:
            self.email = self.user.email
        super(UserCheckout, self).save(*args, **kwargs)


class UserAddress(models.Model):
    """Địa chỉ user"""
    user = models.ForeignKey(UserCheckout, default=None, null=True, blank=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)

    def __unicode__(self):
        return self.address

    def get_full_address(self):
        return '{0}'.format(self.address)


class Order(models.Model):
    """ Đơn hàng """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    shipping_address = models.ForeignKey(UserAddress, related_name='shipping_address', on_delete=models.CASCADE)
    shipping_price = models.PositiveIntegerField(default=0)
    order_total = models.PositiveIntegerField()
    is_completed = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.cart)

    def save(self, *args, **kwargs):
        self.order_total = self.cart.cart_price + self.shipping_price
        super(Order, self).save(*args, **kwargs)

    def complete_order(self):
        self.is_completed = True
        self.save()
