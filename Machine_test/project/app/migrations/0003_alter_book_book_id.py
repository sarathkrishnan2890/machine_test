# Generated by Django 5.0.1 on 2024-01-25 17:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0002_book_book_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='Book_id',
            field=models.CharField(default='0000', max_length=100),
        ),
    ]
