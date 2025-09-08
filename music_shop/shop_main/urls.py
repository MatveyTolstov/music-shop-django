from django.urls import path
from .views import GenreList, ProductList, CustomLoginView


urlpatterns = [
    path("", GenreList.as_view(), name="main"),
    path("catalog/", ProductList.as_view(), name="catalog"),
    path("login/", CustomLoginView.as_view(), name="login"),
    # path('signup/', SignUpView.as_view(), name='signup'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    
]
