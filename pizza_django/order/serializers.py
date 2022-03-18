from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from product.serializers import ContentsSerializer
from .models import Order, OrderItem


class MyOrderItemSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    contents = ContentsSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "contents",
            "total_price",
            "quantity"
        )


class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "postcode",
            "place",
            "phone",
            "items",
            "created_at",
            "paid_amount",
        )


class OrderItemSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    contents = ContentsSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "contents",
            "total_price",
            "quantity",
        )


class OrderSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "postcode",
            "place",
            "phone",
            "items"
        )

