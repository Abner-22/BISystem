from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe

# Creación del modelo Persona
class Persona (models.Model):
    opciones_genero = (('M', 'Masculino'), ('F', 'Femenino'), )
    nombres = models.CharField('Nombres', max_length=50, help_text='Ingresar solo los nombres')
    apellidos = models.CharField('Apellidos', max_length=50, help_text='Ingresar solo los apellidos')
    genero = models.CharField('Género', max_length=1, choices=opciones_genero, default='M')
    fecha_nacimiento = models.DateField('Fecha de nacimiento', help_text='Ejemplo: 01/01/1991')
    cui = models.CharField('CUI', max_length=17, help_text="Código que se encuentra en el DPI de cada persona")

    """
    Funcion que calcula la edad cada persona según su fecha de nacimiento.
    El resultado de la fecha actual menos la fecha de nacimiento se dividirá dentro de 365.25 tomando en cuanta que cada 4 años 
    hay un día extra, ese día extra se dividirá dentro de 4 y el resultado se sumará a los 365 dias que tiene un año normal.
    """

    def edad (self) :
        edad = int((datetime.now().date() - self.fecha_nacimiento).days / 365.25)
        return '%s años' % edad

    #Función que une los nombres y los apellidos de las personas y retorna su nombre completo
    def nombrecompleto(self) :
        nombre = "{0} {1}"
        return nombre.format(self.nombres, self.apellidos)

    #Función por defecto que retorna en nombre completa de las personas
    def __str__(self):
        return self.nombrecompleto()

    class Meta:
        abstract = True #El atributo abstract permite que la clase persona pueda ser usada para heredar a otra clase.
        unique_together = [('nombres','apellidos'),]
