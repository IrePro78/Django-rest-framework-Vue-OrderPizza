# Generated by Django 4.0.1 on 2022-01-17 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='stripe_token',
        ),
    ]