# Generated by Django 4.2.13 on 2024-05-17 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_review_created_at_review_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]