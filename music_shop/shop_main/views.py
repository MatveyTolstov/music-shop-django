from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from .models import (
    Category,
    Product,
    Manufacturer,
    ProductImage,
    OrderItem,
    Orders,
    Reviews,
)


class CategoryList(ListView):
    model = Category
    context_object_name = "category"


def check(request):
    return HttpResponse("hui")
