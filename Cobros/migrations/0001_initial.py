# Generated by Django 3.0 on 2020-09-20 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Vendedores', '0002_auto_20200920_0932'),
        ('Ventas_Credito', '0006_auto_20200915_2209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cobros',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('cuota', models.PositiveIntegerField(verbose_name='Cuota Q.')),
                ('saldo', models.PositiveIntegerField(default=0, verbose_name='Saldo Q.')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vendedores.Vendedor', verbose_name='Cobrador')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ventas_Credito.VentaCredito', verbose_name='Venta')),
            ],
            options={
                'verbose_name': 'Cuota',
                'verbose_name_plural': 'Cuotas',
                'db_table': 'cobro',
            },
        ),
    ]
