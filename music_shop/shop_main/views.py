from django.shortcuts import render, HttpResponse
from .models import (
    Category,
    Product,
    Manufacturer,
    ProductImage,
    OrderItem,
    Orders,
    Reviews,
)


def check(request):
    return HttpResponse("hui")
