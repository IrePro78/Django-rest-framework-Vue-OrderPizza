from rest_framework import status, authentication, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer
from .tasks import send_mail_task
from django.template import Context
from django.template.loader import get_template


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

    # @staticmethod
    def send_message_order(self, serializer, request):
        to_email = serializer.validated_data['email']
        from_email = 'order@pizza.pl'
        subject = 'Order Pizza Online'
        #
        # for item in request.data['items']:
        #     print(f"Name product: {item['contents']['product_variant']['product']['name']},"
        #           f" Size: {item['contents']['product_variant']['variant']['size']},"
        #           f" Toppings: {[name['name'] for name in item['contents']['toppings']]},"
        #           f" Sauces: {[name['name'] for name in item['contents']['sauces']]},"
        #           f" Quantity: {item['quantity']},")
        # print(serializer.data)
        ser = str(serializer.validated_data['items'])
        # ser = serializer.validated_data['order']
        # print(ser)
        text = get_template("emails/order_conf.html")
        text.render(Context({'id': ser}))

        msg = (subject, text, from_email, [to_email])

        send_mail_task.delay(msg)


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
