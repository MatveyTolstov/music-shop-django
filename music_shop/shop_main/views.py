from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.db.models import Q
from .models import (
    Genre,
    Artist,
    Product,
    OrderItem,
    Order,
    Review,
)


def check(request):
    return render(request, "main.html")


class GenreList(ListView):
    model = Genre
    context_object_name = "genres"
    template_name = "main.html"


class ProductList(ListView):
    model = Product
    context_object_name = "products"
    template_name = "catalog.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        genre_filter = self.request.GET.get("genre")
        if genre_filter:
            queryset = queryset.filter(genre__genre_name=genre_filter)

        artist_filter = self.request.GET.get("artist")
        if artist_filter:
            queryset = queryset.filter(artist__id=artist_filter)

        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(product_name__icontains=search)
                | Q(artist__artist_name__icontains=search)
            )

        sort_by = self.request.GET.get("sort", "created_at")
        if sort_by in [
            "price",
            "-price",
            "product_name",
            "-product_name",
            "created_at",
            "-created_at",
        ]:
            queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        context["artists"] = Artist.objects.all()
        context["current_genre"] = self.request.GET.get("genre")
        context["current_artist"] = self.request.GET.get("artist")
        context["current_min_price"] = self.request.GET.get("min_price")
        context["current_max_price"] = self.request.GET.get("max_price")
        context["current_sort"] = self.request.GET.get("sort", "created_at")
        return context


class ArtistList(ListView):
    model = Artist
    context_object_name = "artists"


class UserDetail(ListView):
    model = User
    context_object_name = "user"
    template_name = "login.html"


class LoginForm(CreateView):
    form_class = SignUpForm
