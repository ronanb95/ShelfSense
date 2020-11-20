# Generated by Django 3.0.3 on 2020-11-20 14:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0008_auto_20201120_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockcontrol',
            name='barcode',
        ),
        migrations.AddField(
            model_name='stockcontrol',
            name='barcode',
            field=models.OneToOneField(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='mainApp.Product'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='stockcontrol',
            name='location',
        ),
        migrations.AddField(
            model_name='stockcontrol',
            name='location',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='mainApp.Location'),
            preserve_default=False,
        ),
    ]