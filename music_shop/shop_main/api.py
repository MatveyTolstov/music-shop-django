from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser

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
from .serializers import (
    GenreSerializer,
    ArtistSerializer,
    ProductSerializer,
    OrderSerializer,
    OrderItemSerializer,
    ReviewSerializer,
    ShippingAddressSerializer,
    CouponSerializer,
)
 


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ["genre_name"]


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ["artist_name"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("genre", "artist").all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ["product_name"]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("user", "shipping_address", "coupon").all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ["status"]

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save()


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related("order", "product").all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ["product__product_name"]

    def get_queryset(self):
        return self.queryset


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("user", "product").all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ["text"]

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save()


class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.select_related("user").all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ["city"]

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save()


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ["code"]


router = DefaultRouter()
router.register(r"genres", GenreViewSet, basename="genre")
router.register(r"artists", ArtistViewSet, basename="artist")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"order-items", OrderItemViewSet, basename="orderitem")
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"addresses", ShippingAddressViewSet, basename="shippingaddress")
router.register(r"coupons", CouponViewSet, basename="coupon")

