# Generated by Django 4.1.1 on 2022-11-19 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='address',
            field=models.CharField(default='some string', max_length=30),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='fullname',
            field=models.CharField(default='some string', max_length=30),
        ),
    ]
