from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    Review,
    ShippingAddress,
    Artist,
    Genre,
    Product,
    Order,
    OrderItem,
    Coupon,
)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text="Обязательное поле. Введите действующий email.",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите ваш email"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите имя пользователя",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите пароль"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Подтвердите пароль"}
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите имя пользователя",
                "autocomplete": "username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите пароль",
                "autocomplete": "current-password",
            }
        )
    )


class ReviewForm(forms.ModelForm):
    rating = forms.FloatField(
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "step": "0.5", "min": "0", "max": "5"}
        ),
        label="Оценка",
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Поделитесь впечатлениями о пластинке...",
            }
        ),
        label="Комментарий",
    )

    class Meta:
        model = Review
        fields = ("rating", "text")


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ("full_name", "phone", "city", "address_line", "postal_code")
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Иванов Иван Иванович"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+7 (999) 999-99-99"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Москва"}
            ),
            "address_line": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ул. Примерная, д. 1, кв. 1",
                }
            ),
            "postal_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "123456"}
            ),
        }
        labels = {
            "full_name": "ФИО",
            "phone": "Телефон",
            "city": "Город",
            "address_line": "Адрес",
            "postal_code": "Почтовый индекс",
        }


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ("code", "discount_percent", "active", "valid_from", "valid_to")
        widgets = {
            "code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите промокод"}
            ),
            "discount_percent": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "max": "100", "step": "1"}
            ),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "valid_from": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "valid_to": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
        }
        labels = {
            "code": "Промокод",
            "discount_percent": "Процент скидки",
            "active": "Активен",
            "valid_from": "Действует с",
            "valid_to": "Действует до",
        }


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ("artist_name", "country")
        widgets = {
            "artist_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название исполнителя",
                }
            ),
            "country": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите страну"}
            ),
        }
        labels = {
            "artist_name": "Исполнитель",
            "country": "Страна",
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ("genre_name", "description")
        widgets = {
            "genre_name": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Описание жанра...",
                }
            ),
        }
        labels = {
            "genre_name": "Жанр",
            "description": "Описание",
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "product_name",
            "description",
            "price",
            "stock_quantity",
            "picture",
            "genre",
            "artist",
        )
        widgets = {
            "product_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Название альбома или пластинки",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Описание продукта...",
                }
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "0"}
            ),
            "stock_quantity": forms.NumberInput(
                attrs={"class": "form-control", "min": "0"}
            ),
            "picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "genre": forms.Select(attrs={"class": "form-select"}),
            "artist": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "product_name": "Название продукта",
            "description": "Описание",
            "price": "Цена",
            "stock_quantity": "Количество на складе",
            "picture": "Изображение",
            "genre": "Жанр",
            "artist": "Исполнитель",
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("status", "shipping_address", "coupon")
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "shipping_address": forms.Select(attrs={"class": "form-select"}),
            "coupon": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "status": "Статус заказа",
            "shipping_address": "Адрес доставки",
            "coupon": "Промокод",
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ("product", "quantity")
        widgets = {
            "product": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control", "min": "1", "value": "1"}
            ),
        }
        labels = {
            "product": "Товар",
            "quantity": "Количество",
        }


class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Поиск по товарам...",
                "aria-label": "Search",
            }
        ),
    )
