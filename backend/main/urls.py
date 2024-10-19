from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path("", home, name="home"),
    path("create/", create_order, name="order_create"),
    path("order/<int:pk>/", order_detail, name="order_detail"),
]
