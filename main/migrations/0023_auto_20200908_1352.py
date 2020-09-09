# Generated by Django 3.1 on 2020-09-08 20:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0022_auto_20200908_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='upvotes',
            field=models.ManyToManyField(blank=True, related_name='upvotes', to=settings.AUTH_USER_MODEL),
        ),
    ]
