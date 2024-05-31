from django.shortcuts import render
from .models import Category, Product

from django.http import response

def shop_page(request):
    category = Category.objects.all()
    products = Product.objects.filter(is_draft=False)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/shop.html', context)


def product_details(request, product_id):
    product_details = Product.objects.get(id=product_id)
    ctg = Category.objects.get(name=product_details.category)
    related_products = Product.objects.filter(category=ctg)
    context = {
        'product': product_details,
        'related_products': related_products
    }
    return render(request, 'shop/product-details.html', context)


def wishlist(request):
    return render(request, 'shop/wishlist.html')

from django.shortcuts import get_object_or_404, render
from .models import Product

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop/product-details.html', {'product': product})


