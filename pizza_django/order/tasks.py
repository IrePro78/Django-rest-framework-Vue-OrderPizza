from celery import shared_task
from django.core.mail import send_mail, EmailMessage


@shared_task
def send_mail_task(msg):

    return send_mail(*msg)
