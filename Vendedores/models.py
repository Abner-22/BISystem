#Importaciones desde django
from django.db import models
from django.utils.safestring import mark_safe

#Importaciones desde los modulos existentes
from Persona.models import *
from Telefono.models import  *
from Municipio.models import *

#Crear la clase vendedor tomando como base la  clase abstracta Persona
class Vendedor (Persona) :
    codigo = models.CharField('Código de vendedor', max_length=10,
                    help_text='Ejemplo: EMP-001')
    municipio = models.ForeignKey(Municipio, on_delete = models.CASCADE,
                    verbose_name = 'Municipio')
    direccion = models.CharField('Dirección de Residencia', max_length=100)
    correo = models.EmailField('Correo Electrónico', max_length=254)
    estado = models.BooleanField('Estado', default=True)

    def __str__(self):
        return self.nombrecompleto()

    def Departamento (self):
        return self.municipio.departamento

    class Meta:
        db_table = 'vendedor'
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'

#Creación del modelo número de teléfono
class NumeroTelefonico (Telefono):
    vendedor = models.ForeignKey(Vendedor, on_delete = models.CASCADE, verbose_name = 'Vendedor')
    numero = models.PositiveIntegerField ('Número de Teléfono', help_text='Solo ingresar números')

    def __str__(self):
        return str(self.numero)

    def ClienteNombre (self) :
        return self.cliente.nombrecompleto()

    class Meta:
        db_table = 'telefonosvendedores'
        verbose_name = 'Número de teléfono del vendedor'
        verbose_name_plural = 'Agenda telefónica de vendedores'
        unique_together = ['numero']
