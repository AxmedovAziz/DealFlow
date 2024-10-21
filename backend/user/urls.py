from django.urls import path
from .views import *

urlpatterns = [
    path("", profile, name="profile"),
    path("<int:seller_id>/", profile_detail, name="seller_profile"),
    path(
        "<str:username>/",
        get_orders_by_username,
        name="get_orders_by_username",
    ),
]
