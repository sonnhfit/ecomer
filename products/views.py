import random
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from . import models, mixins, forms
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from products.models import ProductFeatured, Product, Category
# Create your views here.


class CategoryListView(ListView):
    model = models.Category
    template_name = 'products/product_list.html'


class CategoryDetail(DetailView):
    model = models.Category
    template_name = 'products/category_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetail, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        product_set = obj.product_set.all()
        default_products = obj.default_category.all()
        products = (product_set | default_products).distinct()
        context['products'] = products
        return context


class VariationListView(mixins.StaffRequiredMixin, ListView):
    """
    """
    model = models.Variation
    template_name = 'products/variation_list.html'

    def get_queryset(self, *args, **kwargs):
        return models.Variation.objects.filter(product_id=self.kwargs.get('id'))

    def get_context_data(self, *args, **kwargs):
        context = super(VariationListView, self).get_context_data(*args, **kwargs)
        context['formset'] = forms.VariationInventoryFormSet(queryset=self.get_queryset())
        return context

    def post(self, request, *args, **kwargs):
        formset = forms.VariationInventoryFormSet(request.POST)
        print
        formset.is_valid()
        if formset.is_valid():
            # formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                if new_item.title:
                    new_item.product_id = self.kwargs.get('id')
                    new_item.save()
            messages.success(request, 'Success')
            return redirect('product_list')
        raise Http404


class ProductListView(ListView):
    """
    """
    model = models.Product
    template_name = 'products/product_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            queryset = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        return context


class ProductDetailView(View):
    def get(self, request, id):
        featured_image = ProductFeatured.objects.first()
        product = Product.objects.get(id=id)
        category = Category.objects.all()
        product_feature = ProductFeatured.objects.all()
        context = {
            "featured_image": featured_image,
            "product": product,
            "category": category,
            'product_feature': product_feature
        }
        return render(request, 'product_detail.html', context)
