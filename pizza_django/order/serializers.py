from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from product.serializers import ProductVariantSerializer, ToppingSerializer, SauceSerializer
from .models import Order, OrderItem


class MyOrderItemSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    product_variant = ProductVariantSerializer()
    toppings = ToppingSerializer(many=True)
    sauces = SauceSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = (
            "product_variant",
            "toppings",
            "sauces",
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
    sauces = SauceSerializer(many=True)
    toppings = ToppingSerializer(many=True)


    class Meta:
        model = OrderItem
        fields = (
            "product_variant",
            "toppings",
            "sauces",
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

