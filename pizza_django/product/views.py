from django.db.models import Count
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product, Category, ProductVariant, Topping, Sauce
from .serializers import ProductSerializer, CategorySerializer, ToppingSerializer, ProductVariantSerializer,\
    SauceSerializer


class PopularProductsList(APIView):
    def get(self, request, format=None):
        pizzas = Product.objects.filter(category__name='pizza').annotate(
            num_products=Count('items')).order_by('-num_products')[0:4]

        serializer = ProductSerializer(pizzas, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ProductVariantDetail(APIView):
    def get(self, request, product_slug, format=None):
        variants = ProductVariant.objects.filter(product__slug=product_slug).order_by('variant__id')
        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data)


class ProductToppingDetail(APIView):
    def get(self, request, format=None):
            toppings = Topping.objects.all()
            serializer = ToppingSerializer(toppings, many=True)
            return Response(serializer.data)


class ProductSauceDetail(APIView):
    def get(self, request, format=None):
            sauces = Sauce.objects.all()
            serializer = SauceSerializer(sauces, many=True)
            return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
