from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_mail_task(email_msg):
    email_msg = EmailMessage(*email_msg)
    email_msg.content_subtype = 'html'
    return email_msg.send(fail_silently=False)
