# Generated by Django 5.1.2 on 2024-12-05 15:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gimnasio', '0005_alter_membresia_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membresia',
            name='pago',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gimnasio.pago'),
        ),
    ]
