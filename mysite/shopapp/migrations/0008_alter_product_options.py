# Generated by Django 4.1.5 on 2023-02-21 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0007_rename_order_order_products'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'price']},
        ),
    ]
