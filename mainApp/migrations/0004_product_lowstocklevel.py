# Generated by Django 3.0.3 on 2020-11-19 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_auto_20201117_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='lowStockLevel',
            field=models.IntegerField(default=3),
        ),
    ]
