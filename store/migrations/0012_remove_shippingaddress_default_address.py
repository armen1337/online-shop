# Generated by Django 3.1.5 on 2021-02-13 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_shippingaddress_default_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='default_address',
        ),
    ]
