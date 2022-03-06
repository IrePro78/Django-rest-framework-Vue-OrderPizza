from time import sleep
from celery import shared_task
from django.core.mail import send_mail
from pizza_django.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

username = EMAIL_HOST_PASSWORD
password = EMAIL_HOST_USER


@shared_task
def send_mail_task(to_mail):
    # sleep(10)
    send_mail('temat', 'wiadomość', 'admin@gmail.com', [to_mail])
    return None
