# Generated by Django 4.1.5 on 2023-01-27 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0005_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order',
            field=models.ManyToManyField(related_name='orders', to='shopapp.product'),
        ),
    ]
