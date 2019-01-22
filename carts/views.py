from django.shortcuts import render
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse
from orders.models import Order
from . import models
from products import models as product_models
# Create your views here.


class CartCreateView(View):

    """ add item to cart request handler """

    @staticmethod
    def _process_cart(item_id, quantity, delete, request):
        cart = None
        is_deleted = False
        if 'cart_id' not in request.session:
            cart = models.Cart.objects.create()
            request.session['cart_id'] = cart.id

        if cart is None:
            cart = models.Cart.objects.get(id=request.session['cart_id'])
        cart.user = request.user
        cart.save()


        cart_item, created = models.CartItem.objects.get_or_create(cart=cart, item_id=item_id)
        print(cart_item)
        if created or quantity != 1:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += 1
        if delete in ['y','yes', 'true', 'True']:
            is_deleted = True
            cart_item.delete()
        else:
            cart_item.save()
        return cart, is_deleted, cart_item

    def get(self, request):
        try:
            item_id = request.GET.get('item')
            #quantity = request.GET.get('qty', 1)
            quantity = 1
            delete = request.GET.get('delete', 'n')
            cart, is_deleted, cart_item = self._process_cart(item_id, int(quantity), delete, request)
            cart_count = cart.total_count
            request.session['cart_count'] = cart_count
            return HttpResponse('oke')
        except Exception as error:
            print(error)
            return HttpResponse('noke')


class CartDetailView(View):
    template_name = 'card_detail.html'

    def get(self, request):
        if 'cart_id' not in request.session:
            return render(request, self.template_name, {'object': None})

        print(request.session['cart_id'])
        cart = models.Cart.objects.get(id=request.session['cart_id'])
        return render(request, self.template_name, {'object': cart})


class OrderView(View):

    def post(self, request):
        hoten = request.POST.get("name")
        sodienthoai = request.POST.get("phone_number")
        email = request.POST.get("email")
        diachi = request.POST.get("address")
        user_id = request.id
        order = Order.objects.create(
            cart_id=request.session['cart_id'], user_id=user_id,
            shipping_address=diachi, order_total= , is_completed=False)
        return render(request, 'checkout_oke.html')



