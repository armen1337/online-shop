# Generated by Django 3.1.5 on 2021-02-09 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_order_total'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Заказанный продукт', 'verbose_name_plural': 'Заказанные продукты'},
        ),
    ]