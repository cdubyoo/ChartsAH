# Generated by Django 3.1 on 2020-09-18 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_message_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='subject',
        ),
    ]