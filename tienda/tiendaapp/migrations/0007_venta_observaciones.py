# Generated by Django 5.1.2 on 2024-10-13 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaapp', '0006_alter_cliente_saldo'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='observaciones',
            field=models.TextField(null=True),
        ),
    ]
