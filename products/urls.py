from django.urls import path
from . import views as product_view
from django.urls import re_path

urlpatterns = [
    re_path(r'^$', product_view.ProductListView.as_view(), name='product_list'),
    re_path(r'^categories/$', product_view.CategoryListView.as_view(), name='category_list'),
    re_path(r'^categories/(?P<slug>[\w-]+)/$', product_view.CategoryDetail.as_view(), name='category_detail'),
    re_path(r'^(?P<id>[\w-]+)/$', product_view.ProductDetailView.as_view(), name='product_detail'),
    re_path(r'^(?P<id>[\w-]+)/variation/?', product_view.VariationListView.as_view(), name='variation_list'),
]
