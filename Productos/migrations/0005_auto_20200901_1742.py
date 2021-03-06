# Generated by Django 3.0 on 2020-09-01 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0004_auto_20200817_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='existencias',
            field=models.PositiveIntegerField(default=1, help_text='Solo ingresar números enteros positivos', verbose_name='Cantidad de existencias'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AgregarExistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True, verbose_name='Fecha de ingreso')),
                ('cantidad', models.PositiveIntegerField(verbose_name='Cantidad que ingresó')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Productos.Producto', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Agregar existencia',
                'verbose_name_plural': 'Agregar existencias',
                'db_table': 'agregar_existencia',
            },
        ),
    ]
