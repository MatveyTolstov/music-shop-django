from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from rest_framework.filters import SearchFilter

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
from .permissions import IsStaffOrReadOnly, IsOwnerOrStaffOrReadOnly


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["genre_name"]


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["artist_name"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("genre", "artist").all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["product_name"]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("user", "shipping_address", "coupon").all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["status"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        return Order.objects.none()

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related("order", "product").all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["product__product_name"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        if user.is_authenticated:
            return self.queryset.filter(order__user=user)
        return OrderItem.objects.none()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("user", "product").all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["text"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        return Review.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.select_related("user").all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["city"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        return ShippingAddress.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsStaffOrReadOnly]
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

