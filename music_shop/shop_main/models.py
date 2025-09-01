from django.db import models
from django.contrib.auth.models import User


def max_choices_len(choices):
    return max(len(i) for i in choices)


class Category(models.Model):
    class CategoryChoices(models.TextChoices):
        ACOUSTIC_GUITAR = "acoustic guitars", "Акустические гитары"
        ELECTRIC_GUITAR = "electric guitars", "Электро гитары"
        CLASSIC_GUITAR = "classic guitars", "Классические гитары"
        BASS_GUITAR = "bass guitars", "Бас гитары"
        ACOUSTIC_BASS_GUITAR = "acoustic bass guitars", "Акустические бас гитары"
        STRINGS = "strings", "Струны"

    category_name = models.CharField(
        max_length=max_choices_len(CategoryChoices.values), choices=CategoryChoices
    )
    description = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.category_name


class Manufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=100)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.manufacturer_name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("product_name", "manufacturer")

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return "image for {}".format(self.product.product_name)


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_order = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)


class Reviews(models.Model):
    rating = models.FloatField()
    text = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
