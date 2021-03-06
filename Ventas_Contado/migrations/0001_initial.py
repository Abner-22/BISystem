# Generated by Django 3.0 on 2020-08-08 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Productos', '0001_initial'),
        ('Clientes', '0002_auto_20200805_2036'),
        ('Vendedores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VentaContado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True, verbose_name='Fecha')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=7, verbose_name='total')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Clientes.Cliente')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vendedores.Vendedor')),
            ],
            options={
                'verbose_name': 'Venta al contado',
                'verbose_name_plural': 'Ventas al contado',
                'db_table': 'venta_contado',
            },
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Productos.Producto', verbose_name='Producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ventas_Contado.VentaContado', verbose_name='Venta')),
            ],
            options={
                'verbose_name': 'Detalle de la venta al contado',
                'verbose_name_plural': 'Detalles de las ventas al contado',
                'db_table': 'detalle_ventacontado',
            },
        ),
    ]
