from django import forms
from .models import Order, OrderItem
from django.contrib.auth.models import User


class OrderForm(forms.ModelForm):
    seller = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Seller",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Order
        fields = ["seller", "description"]
        widgets = {
            # "seller": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["name", "brand", "size", "quantity", "color"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "brand": forms.TextInput(attrs={"class": "form-control"}),
            "size": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
        }
