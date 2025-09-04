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
    context_object_name = "categories"


class ProductList(ListView):
    model = Product
    context_object_name = "products"


class Manufacturer(ListView):
    model = Manufacturer
    context_object_name = "manufacturers"
