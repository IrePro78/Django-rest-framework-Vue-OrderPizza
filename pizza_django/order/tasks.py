from time import sleep
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail_task(msg):
    print(msg)
    # sleep(10)
    send_mail(*msg)
    return None
