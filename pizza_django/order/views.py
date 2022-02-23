from rest_framework import status, authentication, permissions, viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from product.models import Topping
from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer, OrderItemSerializer


class CheckoutView(GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            paid_amount = sum(item.get('total_price') for item in serializer.validated_data['items'])
            serializer.save(user=request.user, paid_amount=paid_amount)

            print(paid_amount)

        return Response(serializer.data, status=status.HTTP_201_CREATED)























# class CheckoutView(GenericAPIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = OrderSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         order = Order.objects.create(serializer)
#         serializer.is_valid(raise_exception=True)
#         for item_data in serializer.data['items']:
#             toppings_data = item_data.get('toppings')
#
#             order_item = OrderItem.objects.create(
#                         order=order,
#                         product_variant=item_data['product_variant'],
#                         total_price=item_data['total_price'],
#                         quantity=item_data['quantity']
#                     )
#             print(serializer)
#             print(toppings_data)

        # for item_data in data:
        #     toppings_data = item_data.get('toppings')
        #
        #     order_item = OrderItem.objects.create(
        #         order=order,
        #         product_variant=item_data['product_variant'],
        #         total_price=item_data['total_price'],
        #         quantity=item_data['quantity']
        #     )
        #
        #     for topping in toppings_data:
        #         topping_obj = Topping.objects.get(name=topping['name'])
        #         order_item.toppings.add(topping_obj)
        #
        # OrderItem.objects.create(order=order, **item_data)
        #
        #
        # paid_amount = sum(item.get('total_price') for item in data.validated_data['items'])
        # data.save(user=request.user, paid_amount=paid_amount)
        #
        # return Response(data.data, status=status.HTTP_201_CREATED)















# class CheckoutView(GenericAPIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = OrderSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         print(serializer)
#         # serializer.save()
#         paid_amount = sum(item.get('total_price') for item in serializer.validated_data['items'])
#         print(paid_amount)
#
#         data = {
#             'paid_amount': paid_amount,
#             'user': request.user
#         }
#
#         return Response(data=data.update(serializer.data), status=status.HTTP_201_CREATED)







class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)

