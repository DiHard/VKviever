# Generated by Django 5.1.3 on 2024-12-01 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VKstorage', '0008_rename_start_date_posts_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='access_token_live',
            field=models.CharField(default=123123, max_length=250, verbose_name='Дата обновления токена'),
            preserve_default=False,
        ),
    ]
