from django.db import models

# Create your models here.

class Producto (models.Model):
    opciones_tipo = (('A', 'Amueblado'), ('M', 'Mueble'), ('S', 'Silla'), )
    tipo = models.CharField('Tipo de producto', max_length = 1, choices = opciones_tipo, default = 'S')
    nombre = models.CharField('Nombre del producto', max_length = 100)
    descripcion = models.TextField('Descripción del Producto', max_length = 250)
    precio_costo = models.PositiveIntegerField ('Precio al costo', help_text='Solo ingresar números enteros positivos')
    precio_contado = models.PositiveIntegerField ('Precio de contado', help_text='Solo ingresar números enteros positivos')
    precio_2pagos = models.PositiveIntegerField ('Precio para 2 pagos', help_text='Solo ingresar números enteros positivos')
    precio_3pagos = models.PositiveIntegerField ('Precio para 3 pagos', help_text='Solo ingresar números enteros positivos')
    precio_plazos = models.PositiveIntegerField ('Precio a plazos', help_text='Solo ingresar números enteros positivos')
    estado = models.BooleanField('Estado', default=True)

    def __str__ (self) :
        return self.nombre

    def PrecioCosto (self):
        return 'Q. %s' % self.precio_costo

    def PrecioContado (self):
        return 'Q. %s' % self.precio_contado

    def Precio2Pagos (self):
        return 'Q. %s' % self.precio_2pagos

    def Precio3Pagos (self):
        return 'Q. %s' % self.precio_3pagos

    def PrecioPlazos (self):
        return 'Q. %s' % self.precio_plazos

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        unique_together = ['nombre']
