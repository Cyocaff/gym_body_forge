# Generated by Django 5.1.2 on 2024-12-05 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gimnasio', '0004_remove_membresia_cliente_membresia_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membresia',
            name='pago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gimnasio.pago', unique=True),
        ),
    ]
