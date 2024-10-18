# Generated by Django 5.1.2 on 2024-10-17 15:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaapp', '0007_venta_observaciones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='productos',
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='tiendaapp.venta'),
        ),
    ]
