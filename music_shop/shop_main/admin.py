from django.contrib import admin
from .models import (
    Product,
    Genre,
    Artist,
    OrderItem,
    Order,
    Review,
)


# Register your models here.
@admin.register(Artist, Genre, OrderItem, Order, Review)
class ShopAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = [
        "product_name",
        "price",
        "genre",
        "artist",
    ]
    list_filter = ["genre", "artist"]
    search_fields = ["product_name"]


admin.site.register(Product, ProductAdmin)
