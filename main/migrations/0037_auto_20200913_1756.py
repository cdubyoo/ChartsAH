# Generated by Django 3.1 on 2020-09-14 00:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_auto_20200913_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_traded',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
