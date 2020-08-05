from django.db import models

# Create your models here.

class Telefono (models.Model):
    opciones_tipo = (('C','Celular'),('P','Particular'),('L','Laboral'),('R','Residencial'),('O','Otro'))
    tipo = models.CharField('Tipo número telefónico', choices=opciones_tipo, max_length=1, default='C', help_text='Elegir el tipo de número telefónico. Ej. Celular')

    def __str__(self):
        return self.tipo

    class Meta:
        abstract = True
