# Generated by Django 4.2.12 on 2024-05-08 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_book_book_format_book_book_type_book_cover_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_books', to='main.book')),
                ('recommended', models.ManyToManyField(related_name='recommendations_for', to='main.book')),
            ],
        ),
    ]