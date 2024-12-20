# Generated by Django 5.1.3 on 2024-11-26 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VKstorage', '0007_posts_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='start_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='stories',
            old_name='start_date',
            new_name='date',
        ),
        migrations.AddField(
            model_name='posts',
            name='unix_date',
            field=models.IntegerField(default=1, verbose_name='Дата и время публикации UNIX'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stories',
            name='unix_date',
            field=models.IntegerField(default=1234, verbose_name='Дата и время публикации UNIX'),
            preserve_default=False,
        ),
    ]
