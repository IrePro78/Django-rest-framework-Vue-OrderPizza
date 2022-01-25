from rest_framework import serializers

from .models import Category, Product, Sauce, Size, Topping


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.CharField(source="size.price.price")
    # size = serializers.CharField(source="size.name")


    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "size",
            "get_image",
            "get_thumbnail"
        )
        depth = 2


class SauceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sauce
        fields = (
            "id",
            "name",
            "price"
        )


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = (
            "id",
            "name",
            "price"
        )


class SizePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = (
            "id",
            "name",
            "price"
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
        )
