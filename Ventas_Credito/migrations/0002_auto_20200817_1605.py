# Generated by Django 3.0 on 2020-08-17 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas_Credito', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventacredito',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7, verbose_name='Saldo Q.'),
        ),
        migrations.AlterField(
            model_name='ventacredito',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7, verbose_name='Total Q.'),
        ),
    ]
