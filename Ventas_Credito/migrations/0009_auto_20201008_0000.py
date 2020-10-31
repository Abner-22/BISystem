# Generated by Django 3.0 on 2020-10-08 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas_Credito', '0008_auto_20201001_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleventacredito',
            name='subtotal',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='detalleventacredito',
            name='cantidad',
            field=models.PositiveIntegerField(help_text='Solo enteros positivos'),
        ),
        migrations.AlterField(
            model_name='ventacredito',
            name='enganche',
            field=models.PositiveIntegerField(default=0, help_text='Ingresar solo números enteros', verbose_name='Enganche'),
        ),
        migrations.AlterField(
            model_name='ventacredito',
            name='saldo',
            field=models.PositiveIntegerField(default=0, verbose_name='Saldo'),
        ),
        migrations.AlterField(
            model_name='ventacredito',
            name='total',
            field=models.PositiveIntegerField(default=0, verbose_name='Total'),
        ),
    ]