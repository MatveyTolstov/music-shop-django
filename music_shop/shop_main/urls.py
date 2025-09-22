from django.urls import path
from . import views

urlpatterns = [
    path("", views.GenreList.as_view(), name="main"),
    path("catalog/", views.ProductList.as_view(), name="catalog"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("overview/<str:model>/", views.AdminOverviewView.as_view(), name="overview"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("account/", views.AccountView.as_view(), name="account"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("genres/", views.GenreListView.as_view(), name="genre-list"),
    path("genres/create/", views.GenreCreateView.as_view(), name="genre-create"),
    path("genres/<int:pk>/", views.GenreDetailView.as_view(), name="genre-detail"),
    path(
        "genres/<int:pk>/update/", views.GenreUpdateView.as_view(), name="genre-update"
    ),
    path(
        "genres/<int:pk>/delete/", views.GenreDeleteView.as_view(), name="genre-delete"
    ),
    # Artist CRUD
    path("artists/", views.ArtistListView.as_view(), name="artist-list"),
    path("artists/create/", views.ArtistCreateView.as_view(), name="artist-create"),
    path("artists/<int:pk>/", views.ArtistDetailView.as_view(), name="artist-detail"),
    path("artists/<int:pk>/update/", views.ArtistUpdateView.as_view(), name="artist-update"),
    path("artists/<int:pk>/delete/", views.ArtistDeleteView.as_view(), name="artist-delete"),
    # Product CRUD
    path("products/", views.ProductListView.as_view(), name="product-list"),
    path("products/create/", views.ProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/", views.ProductDetailCrudView.as_view(), name="product-detail-crud"),
    path("products/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product-update"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product-delete"),
    # Order CRUD
    path("orders/", views.OrderListView.as_view(), name="order-list"),
    path("orders/create/", views.OrderCreateView.as_view(), name="order-create"),
    path("orders/<int:pk>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:pk>/update/", views.OrderUpdateView.as_view(), name="order-update"),
    path("orders/<int:pk>/delete/", views.OrderDeleteView.as_view(), name="order-delete"),
    # OrderItem CRUD
    path("orderitems/", views.OrderItemListView.as_view(), name="orderitem-list"),
    path("orderitems/create/", views.OrderItemCreateView.as_view(), name="orderitem-create"),
    path("orderitems/<int:pk>/", views.OrderItemDetailView.as_view(), name="orderitem-detail"),
    path("orderitems/<int:pk>/update/", views.OrderItemUpdateView.as_view(), name="orderitem-update"),
    path("orderitems/<int:pk>/delete/", views.OrderItemDeleteView.as_view(), name="orderitem-delete"),
    # Review CRUD
    path("reviews/", views.ReviewListView.as_view(), name="review-list"),
    path("reviews/create/", views.ReviewCreateView.as_view(), name="review-create"),
    path("reviews/<int:pk>/", views.ReviewDetailView.as_view(), name="review-detail"),
    path("reviews/<int:pk>/update/", views.ReviewUpdateView.as_view(), name="review-update"),
    path("reviews/<int:pk>/delete/", views.ReviewDeleteView.as_view(), name="review-delete"),
    # ShippingAddress CRUD
    path("addresses/", views.ShippingAddressListView.as_view(), name="shippingaddress-list"),
    path("addresses/create/", views.ShippingAddressCreateView.as_view(), name="shippingaddress-create"),
    path("addresses/<int:pk>/", views.ShippingAddressDetailView.as_view(), name="shippingaddress-detail"),
    path("addresses/<int:pk>/update/", views.ShippingAddressUpdateView.as_view(), name="shippingaddress-update"),
    path("addresses/<int:pk>/delete/", views.ShippingAddressDeleteView.as_view(), name="shippingaddress-delete"),
    # Coupon CRUD
    path("coupons/", views.CouponListView.as_view(), name="coupon-list"),
    path("coupons/create/", views.CouponCreateView.as_view(), name="coupon-create"),
    path("coupons/<int:pk>/", views.CouponDetailView.as_view(), name="coupon-detail"),
    path("coupons/<int:pk>/update/", views.CouponUpdateView.as_view(), name="coupon-update"),
    path("coupons/<int:pk>/delete/", views.CouponDeleteView.as_view(), name="coupon-delete"),
    # DB overview
    path("db/", views.DatabaseOverviewView.as_view(), name="db-overview"),
]
