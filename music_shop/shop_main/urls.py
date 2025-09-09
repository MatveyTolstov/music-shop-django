from django.urls import path
from .views import (
    GenreList,
    ProductList,
    CustomLoginView,
    SignUpView,
    AccountView,
    CustomLogoutView,
    ProductDetailView,
    CartView,
    AdminOverviewView,
)


urlpatterns = [
    path("", GenreList.as_view(), name="main"),
    path("catalog/", ProductList.as_view(), name="catalog"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("cart/", CartView.as_view(), name="cart"),
    path("overview/<str:model>/", AdminOverviewView.as_view(), name="overview"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("account/", AccountView.as_view(), name="account"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
