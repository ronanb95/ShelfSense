# Generated by Django 3.0.3 on 2020-11-24 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0013_auto_20201124_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockcontrol',
            name='stockControlId',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
