# Generated by Django 4.1.1 on 2022-10-13 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_inventory_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='quantity',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
