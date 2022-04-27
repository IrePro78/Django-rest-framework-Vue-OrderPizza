from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_mail_task(*args):

    email_msg = EmailMessage(*args)
    email_msg.content_subtype = 'html'
    email_msg.send(fail_silently=False)