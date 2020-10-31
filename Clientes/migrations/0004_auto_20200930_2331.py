# Generated by Django 3.0 on 2020-10-01 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0003_auto_20200920_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cui',
            field=models.CharField(help_text='Código que se encuentra en el DPI de cada persona', max_length=17, unique=True, verbose_name='CUI'),
        ),
    ]