from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Review, ShippingAddress


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, 
        help_text="Обязательное поле. Введите действующий email.",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'})
    )


class ReviewForm(forms.ModelForm):
    rating = forms.FloatField(
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
        label='Оценка'
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control text-area',
            'rows': 4,
            'placeholder': 'Поделитесь впечатлениями о пластинке...'
        }),
        label='Комментарий'
    )

    class Meta:
        model = Review
        fields = ("rating", "text")


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ("full_name", "phone", "city", "address_line", "postal_code")
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "address_line": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "full_name": "ФИО",
            "phone": "Телефон",
            "city": "Город",
            "address_line": "Адрес",
            "postal_code": "Индекс",
        }


class CouponForm(forms.Form):
    code = forms.CharField(
        required=False,
        label="Промокод",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите промокод"}),
    )

    # No Meta for simple Form