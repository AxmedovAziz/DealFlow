from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "home.html")


@login_required(login_url="/accounts/login")
def create_order(request):
    OrderItemFormSet = modelformset_factory(OrderItem, form=OrderItemForm, extra=1)

    if request.method == "POST":
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user  # Assign the logged-in user
            order.save()

            for form in formset:
                order_item = form.save(commit=False)
                order_item.order = order  # Link order items to the order
                order_item.save()

            return redirect("home")  # Redirect to the home page or another page

    else:
        order_form = OrderForm()
        formset = OrderItemFormSet(queryset=OrderItem.objects.none())

    return render(
        request, "order_create.html", {"order_form": order_form, "formset": formset}
    )
