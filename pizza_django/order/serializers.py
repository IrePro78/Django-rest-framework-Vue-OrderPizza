from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from product.models import Topping
from product.serializers import ProductVariantSerializer, ToppingSerializer, SauceSerializer
from .models import Order, OrderItem


class MyOrderItemSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    product_variant = ProductVariantSerializer()
    toppings = ToppingSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = (
            "product_variant",
            "toppings",

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
    # sauces = SauceSerializer(many=True)
    toppings = ToppingSerializer(many=True)

    # sauces = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # toppings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # product_variant = ProductVariantSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "product_variant",
            "toppings",

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



    # def create(self, validated_data):
    #     items_data = validated_data.pop('items')
    #     order = Order.objects.create(**validated_data)
    #     print(items_data)
    #     for item_data in items_data:
    #         OrderItem.objects.create(order=order, **item_data)
    #
    #     return order
    #




    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            toppings_data = item_data.get('toppings')

            order_item = OrderItem.objects.create(
                order=order,
                product_variant=item_data['product_variant'],
                total_price=item_data['total_price'],
                quantity=item_data['quantity']
            )

            for topping in toppings_data:
                topping_obj = Topping.objects.get(name=topping['name'])
                order_item.toppings.add(topping_obj)

        OrderItem.objects.create(order=order, **item_data)

        return order
