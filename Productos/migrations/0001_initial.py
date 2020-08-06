# Generated by Django 3.0 on 2020-08-06 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('A', 'Amueblado'), ('M', 'Mueble'), ('S', 'Silla')], default='S', max_length=1, verbose_name='Tipo de producto')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del producto')),
                ('descripcion', models.TextField(max_length=250, verbose_name='Descripción del Producto')),
                ('precio_costo', models.PositiveIntegerField(help_text='Solo ingresar números enteros positivos', verbose_name='Precio al costo')),
                ('precio_contado', models.PositiveIntegerField(help_text='Solo ingresar números enteros positivos', verbose_name='Precio de contado')),
                ('precio_2pagos', models.PositiveIntegerField(help_text='Solo ingresar números enteros positivos', verbose_name='Precio para 2 pagos')),
                ('precio_3pagos', models.PositiveIntegerField(help_text='Solo ingresar números enteros positivos', verbose_name='Precio para 3 pagos')),
                ('precio_plazos', models.PositiveIntegerField(help_text='Solo ingresar números enteros positivos', verbose_name='Precio a plazos')),
                ('estado', models.BooleanField(default='True', verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'db_table': 'producto',
                'unique_together': {('nombre',)},
            },
        ),
    ]
