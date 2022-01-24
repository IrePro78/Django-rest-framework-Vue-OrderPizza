from rest_framework import serializers

from .models import Category, Product, Sauce


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
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
        model = Sauce
        fields = (
            "id",
            "name",
            "price"
        )


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sauce
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
