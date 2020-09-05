# Generated by Django 3.1 on 2020-09-04 23:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0015_auto_20200904_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='follower',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='following',
        ),
        migrations.AddField(
            model_name='follow',
            name='followed',
            field=models.ManyToManyField(null=True, related_name='followed', to=settings.AUTH_USER_MODEL),
        ),
    ]
