# Generated by Django 3.0 on 2020-09-16 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas_Credito', '0005_remove_referencia_cliente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalleventacredito',
            name='engache',
        ),
        migrations.AddField(
            model_name='ventacredito',
            name='enganche',
            field=models.PositiveIntegerField(default=0, help_text='Ingresar solo números enteros', verbose_name='Enganche Q.'),
        ),
        migrations.AlterField(
            model_name='ventacredito',
            name='saldo',
            field=models.PositiveIntegerField(default=0, verbose_name='Saldo Q.'),
        ),
        migrations.AlterField(
            model_name='ventacredito',
            name='total',
            field=models.PositiveIntegerField(default=0, verbose_name='Total Q.'),
        ),
    ]
