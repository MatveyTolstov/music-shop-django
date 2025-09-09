from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, View
from django.contrib.auth.models import User, Group
from .forms import SignUpForm, LoginForm, ReviewForm, ShippingAddressForm, CouponForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
import json
from django.utils import timezone
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


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = "products"
    template_name = "catalog.html"
    login_url = reverse_lazy("login")

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

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        if not product_id:
            return redirect("catalog")
        product = get_object_or_404(Product, pk=product_id)
        if product.stock_quantity <= 0:
            return redirect("catalog")
        cart = {}
        try:
            cart = json.loads(request.COOKIES.get("cart", "{}"))
        except json.JSONDecodeError:
            cart = {}
        cart[str(product.id)] = cart.get(str(product.id), 0) + 1
        response = redirect("catalog")
        response.set_cookie("cart", json.dumps(cart), samesite="Lax")
        return response


class ArtistList(ListView):
    model = Artist
    context_object_name = "artists"


class UserDetail(ListView):
    model = User
    context_object_name = "user"
    template_name = "login.html"


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("account")


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "signup.html"
    success_url = reverse_lazy("account")

    def form_valid(self, form):
        response = super().form_valid(form)
        created_user = self.object
        user_group, _ = Group.objects.get_or_create(name="User")
        created_user.groups.add(user_group)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        return response


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "account.html"
    login_url = reverse_lazy("login")
    redirect_field_name = "next"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group_names = list(user.groups.values_list("name", flat=True))
        is_admin = user.is_superuser or user.is_staff or ("Admin" in group_names)
        context["group_names"] = group_names
        context["role_label"] = "Администратор" if is_admin else "Пользователь"
        # Orders with items
        orders = (
            Order.objects.filter(user=user)
            .prefetch_related("orderitem_set__product")
            .order_by("-date_order")
        )
        orders_data = []
        for o in orders:
            items = []
            total = 0.0
            for it in o.orderitem_set.all():
                subtotal = float(it.price_at_order) * it.quantity
                total += subtotal
                items.append({
                    "product": it.product,
                    "quantity": it.quantity,
                    "price": it.price_at_order,
                    "subtotal": subtotal,
                })
            if o.coupon and o.coupon.active:
                # Apply coupon discount to total for display in account
                percent = o.coupon.discount_percent or 0
                total = total * (1.0 - float(percent) / 100.0)
            orders_data.append({
                "id": o.id,
                "status": o.status,
                "date": o.date_order,
                "items": items,
                "total": total,
            })
        context["orders"] = orders_data
        return context


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("main")


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(product=self.object).select_related("user").order_by("-created_at")
        context["form"] = ReviewForm()
        if self.request.user.is_authenticated:
            context["has_review"] = Review.objects.filter(user=self.request.user, product=self.object).exists()
        else:
            context["has_review"] = False
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "add_to_cart" in request.POST:
            if self.object.stock_quantity <= 0:
                return redirect("product_detail", pk=self.object.pk)
            # cart in cookies
            try:
                cart = json.loads(request.COOKIES.get("cart", "{}"))
            except json.JSONDecodeError:
                cart = {}
            cart[str(self.object.id)] = cart.get(str(self.object.id), 0) + 1
            response = redirect("product_detail", pk=self.object.pk)
            response.set_cookie("cart", json.dumps(cart), samesite="Lax")
            return response

        if not request.user.is_authenticated:
            return redirect("login")
        if Review.objects.filter(user=request.user, product=self.object).exists():
            return redirect("product_detail", pk=self.object.pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                rating=form.cleaned_data["rating"],
                text=form.cleaned_data["text"],
                user=request.user,
                product=self.object,
            )
            return redirect("product_detail", pk=self.object.pk)
        context = self.get_context_data(object=self.object)
        context["form"] = form
        return self.render_to_response(context)


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Read cart from cookies
        try:
            cart = json.loads(self.request.COOKIES.get("cart", "{}"))
        except json.JSONDecodeError:
            cart = {}
        product_ids = [int(pid) for pid in cart.keys()]
        products = {p.id: p for p in Product.objects.filter(id__in=product_ids)}
        items = []
        total = 0.0
        for pid, qty in cart.items():
            pid_int = int(pid)
            product = products.get(pid_int)
            if not product:
                continue
            price = float(product.price)
            subtotal = price * qty
            total += subtotal
            items.append({
                "id": pid_int,
                "product": product,
                "quantity": qty,
                "price": price,
                "subtotal": subtotal,
            })
        context["items"] = items
        context["total"] = total
        # Forms for checkout
        # Pre-fill address from the latest user's address if exists
        initial_address = None
        if self.request.user.is_authenticated:
            from .models import ShippingAddress
            last_addr = ShippingAddress.objects.filter(user=self.request.user).order_by("-created_at").first()
            if last_addr:
                initial_address = {
                    "full_name": last_addr.full_name,
                    "phone": last_addr.phone,
                    "city": last_addr.city,
                    "address_line": last_addr.address_line,
                    "postal_code": last_addr.postal_code,
                }
        context["address_form"] = ShippingAddressForm(initial=initial_address)
        context["coupon_form"] = CouponForm()
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        item_id = request.POST.get("item_id")
        # manipulate cookie cart
        try:
            cart = json.loads(request.COOKIES.get("cart", "{}"))
        except json.JSONDecodeError:
            cart = {}
        response = None
        if action and item_id:
            pid = str(item_id)
            qty = cart.get(pid, 0)
            if action == "inc":
                cart[pid] = qty + 1
            elif action == "dec":
                if qty > 1:
                    cart[pid] = qty - 1
                else:
                    cart.pop(pid, None)
            elif action == "remove":
                cart.pop(pid, None)
            response = redirect("cart")
            response.set_cookie("cart", json.dumps(cart), samesite="Lax")
            return response
        elif action == "checkout":

            if not cart:
                return redirect("cart")

            address_form = ShippingAddressForm(request.POST)
            coupon_form = CouponForm(request.POST)

            coupon_obj = None
            if coupon_form.is_valid():
                code = coupon_form.cleaned_data.get("code", "").strip()
                if code:
                    from .models import Coupon
                    try:
                        coupon_candidate = Coupon.objects.get(code__iexact=code, active=True)
                        now = timezone.now()
                        if (coupon_candidate.valid_from and coupon_candidate.valid_from > now) or (coupon_candidate.valid_to and coupon_candidate.valid_to < now):
                            coupon_obj = None
                        else:
                            coupon_obj = coupon_candidate
                    except Coupon.DoesNotExist:
                        coupon_obj = None

            shipping_address = None
            if address_form.is_valid():
                shipping_address = address_form.save(commit=False)
                shipping_address.user = request.user
                shipping_address.save()
            else:
                context = self.get_context_data()
                context["address_form"] = address_form
                context["coupon_form"] = coupon_form
                return self.render_to_response(context)

            order, _ = Order.objects.get_or_create(user=request.user, status="Pending")

            OrderItem.objects.filter(order=order).delete()
            product_ids = [int(pid) for pid in cart.keys()]
            products = {p.id: p for p in Product.objects.filter(id__in=product_ids)}
            for pid_str, qty in cart.items():
                pid = int(pid_str)
                product = products.get(pid)
                if not product:
                    continue
                if product.stock_quantity < qty:
                    qty = product.stock_quantity
                if qty <= 0:
                    continue
                OrderItem.objects.create(order=order, product=product, quantity=qty, price_at_order=product.price)
                product.stock_quantity -= qty
                product.save()
            order.shipping_address = shipping_address
            if coupon_obj:
                order.coupon = coupon_obj
            order.status = "Placed"
            order.save()
            response = redirect("account")
            response.delete_cookie("cart")
            return response
        return redirect("cart")


class AdminOverviewView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "overview.html"
    login_url = reverse_lazy("login")

    def test_func(self) -> bool:
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_key = self.kwargs.get("model")
        models_map = {
            "genre": Genre,
            "artist": Artist,
            "product": Product,
            "order": Order,
            "orderitem": OrderItem,
            "review": Review,
            "user": User,
        }
        model = models_map.get(model_key)
        if not model:
            raise Http404()
        context["model_name"] = model.__name__
        context["records"] = model.objects.all()[:100]
        context["admin_add_url"] = reverse_lazy("admin:%s_%s_add" % (model._meta.app_label, model._meta.model_name))
        context["admin_changelist_url"] = reverse_lazy("admin:%s_%s_changelist" % (model._meta.app_label, model._meta.model_name))
        context["admin_change_url_name"] = "admin:%s_%s_change" % (model._meta.app_label, model._meta.model_name)
        return context
