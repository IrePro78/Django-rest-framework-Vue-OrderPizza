from rest_framework import serializers

from order.models import ProductVariant
from .models import Category, Product


class ProductVariantSerializer(serializers.ModelSerializer):
    variant = serializers.CharField(source="variant.size")
    product = serializers.CharField(source="product.name")


    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "product",
            "variant",
            "price",
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
