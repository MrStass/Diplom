# Generated by Django 4.2.13 on 2024-05-12 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_book_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]