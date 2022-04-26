from rest_framework import status, authentication, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer
from .tasks import send_mail_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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

        send_message_order(serializer, request)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)


def send_message_order(serializer, request):
    to_email = serializer.validated_data['email']
    from_email = 'order@pizza.pl'
    subject = 'Order Pizza Online'

    order_content = serializer.data
    print(order_content)
    html_content = render_to_string("emails/send_message_order.html", order_content)
    text_content = strip_tags(html_content)

    msg = (subject, text_content, from_email, [to_email], html_content)
    send_mail_task.delay(msg)
