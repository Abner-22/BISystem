#Importaciones desde django
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.html import format_html

#Importaciones desde los modulos existentes
from Persona.models import *
from Telefono.models import  *
from Municipio.models import *

#Crear la clase cliente tomando como base la  clase abstracta Persona
class Cliente (Persona) :
    nit = models.CharField('NIT', max_length=11, help_text='Ejemplo: 1234567-8')
    municipio = models.ForeignKey(Municipio, on_delete = models.CASCADE, verbose_name = 'Ubicación', help_text='Municipio donde se realizó la venta')
    direccion = models.CharField('Dirección de Residencia', max_length=100)
    correo = models.EmailField('Correo Electrónico', max_length=254, blank=True)
    estado = models.BooleanField('Estado', default=True)

    def __str__(self):
        return self.nombrecompleto()

    def Clientes (self):
        return mark_safe(u'<a href="/clientes" target="_blank">Clientes</a>')
    Clientes.short_description = 'Clientes'

    class Meta:
        db_table = 'cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

#Creación del modelo número de teléfono
class NumeroTelefonico (Telefono):
    cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE, verbose_name = 'Cliente')
    numero = models.PositiveIntegerField ('Número de Teléfono', help_text='Solo ingresar números')

    def __str__(self):
        return str(self.numero)

    def ClienteNombre (self) :
        return self.cliente.nombrecompleto()

    class Meta:
        db_table = 'telefonosclientes'
        verbose_name = 'Número de teléfono de cliente'
        verbose_name_plural = 'Agenda telefónica de clientes'
        unique_together = ['numero']
