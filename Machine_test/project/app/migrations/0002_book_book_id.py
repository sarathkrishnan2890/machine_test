# Generated by Django 5.0.1 on 2024-01-25 17:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='Book_id',
            field=models.CharField(default='11111', max_length=100),
        ),
    ]
