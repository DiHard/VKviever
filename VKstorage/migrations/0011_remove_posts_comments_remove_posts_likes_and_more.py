# Generated by Django 5.1.3 on 2024-12-02 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VKstorage', '0010_remove_settings_access_token_live'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='reposts',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='views',
        ),
    ]