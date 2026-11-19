from django.shortcuts import render
from .models import Product


def store(request):
    products = Product.objects.select_related("category").order_by("name")
    return render(request, "main/store.html", {"products": products})
