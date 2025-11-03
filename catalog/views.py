from django.shortcuts import render, get_object_or_404
from .models import Product
from catalog.models import Product


def home(request):
    return render(request, "home.html")
#
#
def contacts(request):
    return render(request, "contacts.html")

# def base(request):
#     return render(request, "base.html")

def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, "products_list.html", context)

def product_detail(request, pk):
    product = get_object_or_404 (Product, pk=pk)
    context = {'product': product}
    return render(request, 'products_detail.html', context)