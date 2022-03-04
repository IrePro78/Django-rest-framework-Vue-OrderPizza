import smtplib

from rest_framework import status, authentication, permissions, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem
from .send_mail import send_mail
from .serializers import OrderSerializer, MyOrderSerializer


class CheckoutView(GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        paid_amount = sum(item.get('total_price') for item in serializer.validated_data['items'])

        to_email = serializer.validated_data['email']

        serializer.validated_data['user'] = request.user
        serializer.validated_data['paid_amount'] = paid_amount
        serializer.save()

        try:

            send_mail(html='blablabla', text='Here is your ***REMOVED*** reset token', subject='***REMOVED*** reset token',
                      from_email='pizza@gmail.com',
                      to_emails=[to_email])
        except smtplib.SMTPException:
            raise

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
