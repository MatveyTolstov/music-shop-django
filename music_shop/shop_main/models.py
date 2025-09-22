from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


def max_len_choices(choices):
    return max(len(i) for i in choices)


class Genre(models.Model):
    class GenreChoices(models.TextChoices):
        ROCK_METAL = "rock and metal", "Рок & Металл"
        JAZZ_BLUES = "jazz and blues", "Джаз & Блюз"
        INDIE_ALTERNATIVE = "indie and alternative", "Инди & Альтернатива"
        POP_DISCO = "pop and disco", "Поп & Диско"
        CLASSICAL = "classical", "Классика"
        RUSSIAN_SOVIET = "russian and soviet", "Русское & Советское"

    genre_name = models.CharField(
        max_length=max_len_choices(GenreChoices.values), choices=GenreChoices.choices
    )
    description = models.TextField()

    def __str__(self):
        return self.get_genre_name_display()


class Artist(models.Model):
    artist_name = models.CharField(max_length=100)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.artist_name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    picture = models.ImageField(upload_to="products/images/", null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product_name", "artist")

    def __str__(self):
        return self.product_name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_order = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")
    shipping_address = models.ForeignKey(
        "ShippingAddress", on_delete=models.SET_NULL, null=True, blank=True
    )
    coupon = models.ForeignKey(
        "Coupon", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return (
            f"{self.quantity} of {self.product.product_name} in Order {self.order.id}"
        )


class Review(models.Model):
    rating = models.FloatField()
    text = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.product_name} by {self.user.username}"


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=80)
    address_line = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name}, {self.city}, {self.address_line}"


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"
