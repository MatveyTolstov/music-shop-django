from django.urls import path
from .views import GenreList, ProductList


urlpatterns = [
    path("", GenreList.as_view(), name="main"),
    path("catalog/", ProductList.as_view(), name="catalog"),
]
