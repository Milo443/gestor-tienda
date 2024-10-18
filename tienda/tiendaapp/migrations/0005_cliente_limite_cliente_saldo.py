# Generated by Django 5.1.2 on 2024-10-12 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaapp', '0004_alter_cuentacredito_limite_alter_cuentacredito_saldo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='limite',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
        migrations.AddField(
            model_name='cliente',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
    ]
