from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from .models import Category, Product, Variant, Topping, ProductVariant, Sauce


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


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = (
            "id",
            "size",
            "description"
        )


class ProductSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "get_absolute_url",
            "description",
            "get_image",
            "get_thumbnail"
        )


class ProductVariantSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    product = ProductSerializer()
    variant = VariantSerializer()

    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "product",
            "variant",
            "is_default",
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
            "products"
        )
