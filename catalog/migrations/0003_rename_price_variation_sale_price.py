# Generated by Django 3.2.5 on 2021-07-28 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_variation_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='price',
            new_name='sale_price',
        ),
    ]
