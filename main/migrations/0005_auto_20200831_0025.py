# Generated by Django 3.1 on 2020-08-31 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_post_post_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post_image',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='post_published',
            new_name='published',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='post_title',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_content',
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
