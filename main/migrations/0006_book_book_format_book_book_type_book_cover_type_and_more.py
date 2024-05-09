# Generated by Django 5.0.4 on 2024-05-02 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_book_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_format',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='book_type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='cover_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='original_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='page_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
