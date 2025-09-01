from django.contrib import admin
from .models import (
    Product,
    Category,
    Manufacturer,
    ProductImage,
    OrderItem,
    Orders,
    Reviews,
)


# Register your models here.
@admin.register(ProductImage, Category, Manufacturer, OrderItem, Orders, Reviews)
class ShopAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = [
        "product_name",
        "price",
        "category",
        "manufacturer",
    ]
    list_filter = ["category", "manufacturer"]
    search_fields = ["product_name"]


admin.site.register(Product, ProductAdmin)
