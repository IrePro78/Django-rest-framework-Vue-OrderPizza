from rest_framework import status, authentication, permissions, viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from product.models import Topping
from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer, OrderItemSerializer


# @api_view(['POST'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
# def checkout(request):
#     serializer = OrderSerializer(data=request.data)
#
#     if serializer.is_valid():
#         # print(serializer)
#         # print(request.data)
#
#         paid_amount = sum(item.get('total_price') for item in serializer.validated_data['items'])
#
#         try:
#             serializer.save(user=request.user, paid_amount=paid_amount)
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         except Exception:
#
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, )
#
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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

    #     items_data = serializer.pop('items')
    #
    #
    # if serializer.is_valid(raise_exception=True):
    #     paid_amount = sum(item.get('total_price') for item in serializer.data['items'])
    #     print(paid_amount)
    #     serializer.save(user=request.user, paid_amount=paid_amount)
    #
    # order_item = OrderItem.objects.create(
    #     product_variant=data['product_variant'],
    #     sauces=data['sauces'],
    #     total_price=data['total_price'],
    #     quantity=data['quantity']
    # )
    # order_item.save()
    #
    # for item_data in items_data:
    #     for topping in item_data['toppings']:
    #         topping_obj = Topping.objects.get(name=topping['name'])
    #         order_item.toppings.add(topping_obj)
    # OrderItem.objects.create(order=order, **order_item)
    #
    # print(serializer)
    # return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)


# class CheckoutViewSet(viewsets.ModelViewSet):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = OrderSerializer
#
#     def get_queryset(self):
#         order = Order.objects.all()
#         return order
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         paid_amount = sum(item.get('total_price') for item in serializer.data['items'])
#         data = {
#             'paid_amount': paid_amount,
#             'user': request.user
#         }
#         return Response(data=data.update(serializer.data), status=status.HTTP_201_CREATED)

# class CheckoutView(GenericAPIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = OrderSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         paid_amount = sum(item.get('total_price') for item in serializer.validated_data['items'])
#         data = {
#             'paid_amount': paid_amount,
#             'user': request.user
#         }
#         print(data)
#         return Response(data=data.update(serializer.data), status=status.HTTP_201_CREATED)
#