from rest_framework import serializers

from order.models import ProductVariant
from .models import Category, Product, Variant


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
            "price",
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
