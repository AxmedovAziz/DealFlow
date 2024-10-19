from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from main.models import Order
from .models import OrderConfirmation


@login_required
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        # Create or get an existing confirmation for this order
        confirmation, created = OrderConfirmation.objects.get_or_create(order=order)
        confirmation.confirmed_by = request.user
        confirmation.confirmed_at = timezone.now()
        confirmation.save()

        # Redirect to the order detail page with correct 'pk' parameter
        return redirect("order_detail", pk=order.id)

    return render(request, "order_confirm.html", {"order": order})


@login_required
def set_price(request, order_id):
    confirmation = get_object_or_404(OrderConfirmation, order__id=order_id)

    if request.method == "POST":
        price = request.POST.get("price")
        confirmation.price = price
        confirmation.save()
        return redirect("order_detail", pk=order_id)  # Redirect to order detail

    return render(request, "order_detail.html", {"order": confirmation.order})


@login_required
def complete_order(request, order_id):
    confirmation = get_object_or_404(OrderConfirmation, order_id=order_id)

    if request.method == "POST":
        # Mark as completed and store completion time
        confirmation.completed = True
        confirmation.completed_at = timezone.now()
        confirmation.save()
        # Redirect to the order detail page after completion
        return redirect("order_detail", pk=confirmation.order.id)

    return render(request, "order_complete.html", {"order": confirmation.order})


@login_required
def completed_orders(request):
    # Get all completed orders
    completed_orders = OrderConfirmation.objects.filter(completed=True)
    return render(
        request, "completed_orders.html", {"completed_orders": completed_orders}
    )
