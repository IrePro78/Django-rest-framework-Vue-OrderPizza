import smtplib
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage

from rest_framework import status, authentication, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, MyOrderSerializer
from .tasks import send_mail_task


class CheckoutView(GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        paid_amount = sum(item.get('total_price') for item in serializer.validated_data['items'])

        serializer.validated_data['user'] = request.user
        serializer.validated_data['paid_amount'] = paid_amount
        serializer.save()

        self.send_message_order(serializer, request)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def send_message_order(serializer, request):
        to_email = serializer.validated_data['email']
        from_email = 'order@pizza.pl'
        subject = 'Order Pizza Online'
        text = str(serializer.validated_data['items'])
        msg = (subject, text, from_email, [to_email])

        send_mail_task.delay(msg)


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
