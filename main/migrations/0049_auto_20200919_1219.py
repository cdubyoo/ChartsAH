# Generated by Django 3.1 on 2020-09-19 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0048_auto_20200919_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='last_message',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_message', to='main.message'),
        ),
    ]
