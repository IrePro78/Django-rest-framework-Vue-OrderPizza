from rest_framework import serializers

from order.models import VariantProduct
from .models import Category, Product


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantProduct
        fields = (
            "id",
            "size",
            "price",
        )


class ProductSerializer(serializers.ModelSerializer):
    # size = serializers.CharField(source="size.size")

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "size",
            "get_image",
            "get_thumbnail",
        )
        depth = 1


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
