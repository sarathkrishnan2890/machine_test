# Generated by Django 5.0.1 on 2024-01-25 17:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0003_alter_book_book_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='user',
        ),
        migrations.AddField(
            model_name='author',
            name='user_name',
            field=models.CharField(default='null', max_length=100),
        ),
    ]