# Generated by Django 3.1.5 on 2021-03-22 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_heroimageconf_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='heroimageconf',
            options={'verbose_name': 'Набор hero картинок', 'verbose_name_plural': 'Наборы hero картинок'},
        ),
        migrations.AlterField(
            model_name='heroimageconf',
            name='enabled',
            field=models.BooleanField(default=False),
        ),
    ]
