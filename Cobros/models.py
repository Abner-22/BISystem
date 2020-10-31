from django.db import models
from django.core.exceptions import ValidationError #Libreria que permite configurar mensajes de alerta o errores.

from Ventas_Credito.models import VentaCredito
from Vendedores.models import Vendedor

# Create your models here.

class Cobros (models.Model):
    fecha = models.DateField('Fecha', auto_now_add = False)
    venta= models.ForeignKey(VentaCredito, on_delete = models.CASCADE, verbose_name='Venta')
    vendedor = models.ForeignKey(Vendedor, on_delete = models.CASCADE, verbose_name='Cobrador')
    cuota = models.PositiveIntegerField('Cuota')
    saldo =models.PositiveIntegerField('Saldo Actual', default=0)

    # def save(self, **kwargs):
    #     id_venta = self.venta_id
    #     venta = VentaCredito.objects.get(id=id_venta)
    #     saldoventa = venta.saldo - self.cuota
    #     self.setSaldo(saldoventa)
    #     self.venta.descontarSaldo(self.cuota)
    #     self.venta.save()
    #     super(Cobros, self).save()

    def save(self, **kwargs):
        id_venta = self.venta_id
        try: # ya existen cuotas sobre la venta
            cuotasv = Cobros.objects.filter(venta_id=id_venta)
            ultima = cuotasv.last() # Obtener la última cuota dada para la venta
            if ultima.pk == self.pk: # Si el id de la última es igual al id en curso, se toma como modificación
                if ultima.cuota < self.cuota: # Si el monto que se esta guardando es mayor al que se ingresó inicialmente
                    diferencia = self.cuota - ultima.cuota # Calcular la diferencia
                    self.saldo = self.saldo - diferencia # Corregimos el saldo de la venta
                    super(Cobros, self).save() # Guardamos los cambios
                elif ultima.cuota > self.cuota: # Si le monto que se esta guardando es menor al que se ingresó inicialmente
                    diferencia = ultima.cuota - self.cuota # Calcular la diferencia
                    self.saldo = self.saldo + diferencia # Corregimos el saldo de la venta
                    super(Cobros, self).save() # Guardamos los cambios
            else: # Cuando se esta registra una nueva cuota para la venta
                self.saldo = ultima.saldo - self.cuota
                super(Cobros, self).save() # Guardamos los cambios
        except: # no existen pagos sobre la venta
            id_venta = self.venta_id
            venta = VentaCredito.objects.get(id=id_venta)
            self.saldo = venta.saldo - self.cuota
            super(Cobros, self).save()

    def clean(self): #Acción que preventiva, sobre la cuota mayor al saldo, antes que se registre la cuota.
        id_venta = self.venta_id
        venta = VentaCredito.objects.get(id=id_venta)
        if self.cuota > venta.saldo:
            raise ValidationError('La cuota ingresada es mayor al saldo actual de la venta.  Saldo actual Q. '+str(venta.saldo))
        super(Cobros, self).clean()

    def __str__(self):
        return str(self.pk)

    def cliente (self):
        id_venta = self.venta_id
        venta = VentaCredito.objects.get(id=id_venta)
        return venta.cliente

    def Saldo1 (self):
        id_venta = self.venta_id
        venta = VentaCredito.objects.get(id=id_venta)
        return 'Q. %s' % venta.saldo

    def setSaldo (self, saldoventa):
        self.saldo = saldoventa

    def Cuota (self):
        return 'Q. %s.00' % self.cuota

    def Saldo (self):
        saldo = 'Q. {}.00'
        return saldo.format(self.saldo)

    class Meta :
        db_table = 'cobro'
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'
