from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from products.models import ProductFeatured, Product, Category

# Create your views here.


class Home(View):
    def get(self, request):
        featured_image = ProductFeatured.objects.first()
        products = Product.objects.all().order_by('?')
        category = Category.objects.all()
        context = {
            "featured_image": featured_image,
            "products": products,
            "category": category
        }

        return render(request, "homepage.html", context)

