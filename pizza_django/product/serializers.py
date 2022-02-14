from rest_framework import serializers
from .models import Category, Product, Variant, Topping, ProductVariant, ProductVariantTopping


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


class ProductSerializer(serializers.ModelSerializer):
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


class ProductVariantSerializer(serializers.ModelSerializer):
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


class ProductVariantToppingSerializer(serializers.ModelSerializer):
    toppings = ToppingSerializer(many=True)
    product_variant = ProductVariantSerializer()

    class Meta:
        model = ProductVariantTopping
        fields = (
            "id",
            "product_variant",
            "toppings",
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
