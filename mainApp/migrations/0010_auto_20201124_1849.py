# Generated by Django 3.0.3 on 2020-11-24 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0009_auto_20201120_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockcontrol',
            name='stockControlId',
        ),
        migrations.AddField(
            model_name='stockcontrol',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]