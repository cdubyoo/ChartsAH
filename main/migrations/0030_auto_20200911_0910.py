# Generated by Django 3.1 on 2020-09-11 16:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0029_auto_20200910_0212'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='upvote',
            unique_together={('user', 'post')},
        ),
    ]
