# Generated by Django 3.1.5 on 2021-02-11 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20210211_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='default_address',
            field=models.BooleanField(default=False, verbose_name='Адрес по умолчанию'),
        ),
    ]
