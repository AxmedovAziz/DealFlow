from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["name", "brand", "size", "quantity", "color"]


class OrderSerializer(serializers.ModelSerializer):
    orders = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["user", "seller", "description", "created", "orders"]

    def create(self, validated_data):
        orders_data = validated_data.pop("orders")
        order = Order.objects.create(**validated_data)
        for order_item_data in orders_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order
