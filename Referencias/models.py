from django.db import models
from Clientes.models import *
from Ventas_Credito.models import *
# Create your models here.

class Referencia (models.Model):
    opciones_relacion = (('A', 'Amigo'),('F', 'Familiar'),('L', 'Compañero de trabajo'),)
    cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE, verbose_name = 'Cliente')
    venta = models.ForeignKey(VentaCredito, on_delete = models.CASCADE, verbose_name = 'Venta')
    nombre = models.CharField('Referencia', max_length=100)
    relacion = models.CharField('Relación', max_length=1, choices=opciones_relacion, default='F')
    numero = models.PositiveIntegerField ('Número de Teléfono', help_text='Solo ingresar números')

    def __str__(self):
        cadena = "{0} {1} {2} {3}"
        return cadena.format(self.cliente, self.relacion, self.nombre, self.numero)

    class Meta:
        db_table = 'referencia'
        verbose_name = 'Referencia'
        verbose_name_plural = 'Referencias'
