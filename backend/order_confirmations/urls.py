from django.urls import path
from .views import *

urlpatterns = [
    path("confirm/<int:order_id>/", confirm_order, name="confirm_order"),
    path("complete/<int:order_id>/", complete_order, name="complete_order"),
    path("completed/", completed_orders, name="completed_orders"),
    path("set_price/<int:order_id>/", set_price, name="set_price"),
]
