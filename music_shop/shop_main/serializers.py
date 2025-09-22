from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Genre,
    Artist,
    Product,
    Order,
    OrderItem,
    Review,
    ShippingAddress,
    Coupon,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "genre_name", "description"]


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id", "artist_name", "country"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "description",
            "price",
            "stock_quantity",
            "picture",
            "genre",
            "artist",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            "id",
            "user",
            "full_name",
            "phone",
            "city",
            "address_line",
            "postal_code",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            "id",
            "code",
            "discount_percent",
            "active",
            "valid_from",
            "valid_to",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "price_at_order"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "date_order",
            "status",
            "shipping_address",
            "coupon",
        ]
        read_only_fields = ["date_order"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "rating", "text", "user", "product", "created_at"]
        read_only_fields = ["created_at"]

