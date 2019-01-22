from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r'^$', views.CartCreateView.as_view(), name='create_cart'),
    re_path(r'^view/$', views.CartDetailView.as_view(), name='cart_detail'),
    re_path(r'^checkout/$', views.OrderView.as_view(), name='cart_checkout'),
]