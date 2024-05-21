# Generated by Django 4.2.13 on 2024-05-20 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_address_remove_order_payment_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Наложений платіж'), ('card', 'Картка')], max_length=20, null=True),
        ),
    ]
