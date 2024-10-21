from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import ProfileForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User


@login_required
def profile(request):
    profile = request.user.profile  # Adjust based on how you link user and profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if request.POST.get("remove_image") == "true":
            # Remove the image and set it to None or a default image
            request.user.profile.image = "default-profile.png"
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")  # Adjust to your profile URL name
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile.html", {"form": form})


from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Profile  # Profile from the relevant app
from main.models import Order, OrderItem  # Order and OrderItem from the relevant app
from order_confirmations.models import OrderConfirmation  # OrderConfirmation model


def profile_detail(request, seller_id):
    profile = get_object_or_404(Profile, user_id=seller_id)

    created_orders = Order.objects.filter(seller=profile.name).order_by("-created")

    confirmed_orders = OrderConfirmation.objects.filter(
        order__seller=profile.name, confirmed_by=profile.user, completed=False
    ).order_by("-confirmed_at")

    completed_orders = OrderConfirmation.objects.filter(
        order__seller=profile.name, confirmed_by=profile.user, completed=True
    ).order_by("-completed_at")

    # Paginate created orders
    paginator = Paginator(created_orders, 5)  # 5 orders per page
    page_number = request.GET.get("page")
    paginated_orders = paginator.get_page(page_number)

    context = {
        "profile": profile,
        "created_orders": paginated_orders,
        "confirmed_orders": confirmed_orders,
        "completed_orders": completed_orders,
    }

    return render(request, "seller_profile.html", context)


@login_required
def get_orders_by_username(request, username):
    # Get the user by username
    user = get_object_or_404(User, username=username)

    # Get the user's profile
    profile = get_object_or_404(
        Profile, user=user
    )  # Use user object to get the profile

    # Get the orders for the user
    orders = Order.objects.filter(user=user).order_by("-created")

    # Fetch confirmed but not completed orders
    confirmed_orders = (
        OrderConfirmation.objects.filter(completed=False)
        .order_by("-confirmed_at")
        .select_related("order", "confirmed_by")
    )

    # Fetch completed orders
    completed_orders = (
        OrderConfirmation.objects.filter(completed=True)
        .order_by("-completed_at")
        .select_related("order", "confirmed_by")
    )

    # Render the orders in response to the HTMX request
    return render(
        request,
        "user_orders.html",
        {
            "confirmed_orders": confirmed_orders,
            "profile": profile,
            "completed_orders": completed_orders,
            "orders": orders,  # Include your existing orders if needed
        },
    )
