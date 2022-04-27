from django.core.mail import EmailMessage
from rest_framework import status, authentication, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer
from .tasks import send_mail_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
    print(to_email)
    html_content = render_to_string("emails/send_message_order.html", order_content)

    email_msg = (subject, html_content, from_email, [to_email, ])

    email_msg = EmailMessage(*email_msg)
    email_msg.content_subtype = 'html'
    email_msg.send(fail_silently=False)

    # send_mail_task.delay(email_msg)



    # msg_text = MIMEText(text_content, 'plain')
    # msg_html = MIMEText(html_content, 'html')
    #
    # msg = MIMEMultipart('alternative')
    # msg['Subject'] = 'test HTML Email'
    # msg['From'] = from_email
    # msg['To'] = [to_email, ]
    # msg.attach(msg_text)
    # msg.attach(msg_html)
    #
    #
    # msg = (subject, from_email, [to_email], msg.as_string())
    # send_mail_task.delay(msg)









    # order_content = serializer.data
    # print(order_content)
    # html_content = render_to_string("emails/send_message_order.html", order_content)
    # text_content = strip_tags(html_content)
    #
    # msg = (subject, text_content, from_email, [to_email], html_content)
    # send_mail_task.delay(msg)
