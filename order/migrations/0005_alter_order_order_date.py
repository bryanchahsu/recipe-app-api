# Generated by Django 4.1.1 on 2023-11-23 21:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
