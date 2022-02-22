from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from product.models import Topping
from product.serializers import ProductVariantSerializer, ToppingSerializer, SauceSerializer
from .models import Order, OrderItem


class MyOrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer()
    toppings = ToppingSerializer(many=True)

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


class OrderItemSerializer(serializers.ModelSerializer):
    # sauces = SauceSerializer(many=True)
    # toppings = ToppingSerializer(many=True)
    sauces = serializers.PrimaryKeyRelatedField(read_only=True)
    toppings = serializers.PrimaryKeyRelatedField(read_only=True)

    # product_variant = ProductVariantSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "product_variant",
            "toppings",
            "sauces",
            "total_price",
            "quantity",
        )


class OrderSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        print(items_data)
        #
        # for item_data in items_data:
        #     # print(item_data)
        #     order_item = OrderItem.objects.create(
        #         product_variant=item_data['product_variant'],
        #         total_price=item_data['total_price'],
        #         quantity=item_data['quantity']
        #     )
        #
        #     order_item.save()
        #
        #     for topping in item_data['toppings']:
        #         topping_obj = Topping.objects.get(name=topping['name'])
        #         print(topping_obj)
        #         order_item.toppings.add(topping_obj)
        #     OrderItem.objects.create(order=order, **item_data)
        #
        # return order
        #
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
