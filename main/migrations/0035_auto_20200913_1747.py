# Generated by Django 3.1 on 2020-09-14 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_post_date_traded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_traded',
            field=models.DateField(),
        ),
    ]
