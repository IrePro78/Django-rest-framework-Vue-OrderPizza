from rest_framework import serializers

from .models import Category, Product, Sauce, Size, Price, Topping


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(source="size.price.price", max_digits=6, decimal_places=2)
    size = serializers.CharField(source="size.name")

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


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = (
            "id",
            "name",
            "price"
        )


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
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
