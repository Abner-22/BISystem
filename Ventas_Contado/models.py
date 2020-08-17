from django.db import models
from django.core.exceptions import ValidationError

#Importaciones desde los modulos existentes
from Clientes.models import *
from Vendedores.models import *
from Productos.models import *

#Cración de la clase para las ventas al contado
class VentaContado (models.Model) :
    fecha = models.DateField('Fecha', auto_now_add = True)
    cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete = models.CASCADE)
    total = models.DecimalField('total', max_digits=7, decimal_places=2, default=0.00 )

    def __str__(self):
        cadena = "{0} {1} {2}"
        return cadena.format(self.fecha, self.cliente, self.vendedor)

    def Total (self):
        return 'Q. %s' % self.total

    def agregarTotal (self, total):
        self.total += total

    def descontarTotal (self, total):
        self.total -= total

    def save(self, **kwargs):
        super(VentaContado, self).save()

    def Nit (self):
        return self.cliente.nit

    def ID (self):
        return self.id

    class Meta :
        db_table = 'venta_contado'
        verbose_name = 'Venta al contado'
        verbose_name_plural = 'Ventas al contado'

class DetalleVenta (models.Model):
    venta = models.ForeignKey(VentaContado, on_delete=models.CASCADE, verbose_name = 'Venta')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name = 'Producto')
    cantidad = models.PositiveIntegerField()

    '''Función para capturar el total de la venta y poder modificarlo
        El total nos servirá para  
    '''
    def save(self, **kwargs):
        total = self.venta.total
        id_producto = self.producto.pk
        id_venta = self.venta.pk
        if total == 0 :
            #self.producto.descontarStock(self.cantidad)
            self.venta.total = self.venta.total + (self.producto.precio_contado * self.cantidad)
        else:
            try:
                item = DetalleVenta.objects.get(venta=id_venta, producto=id_producto)
                if item.cantidad > self.cantidad:
                    diferencia = item.cantidad - self.cantidad
                    #self.producto.agregarStock(diferencia)
                    total=self.producto.precio_contado * self.cantidad
                    self.venta.descontarTotal(total)
                else:
                    diferencia = self.cantidad - item.cantidad
                    #self.producto.descontarStock(diferencia)
                    total=self.producto.precio_contado * diferencia
                    self.venta.agregarTotal(total)
            except:
                #self.producto.descontarStock(self.cantidad)
                self.venta.total = self.venta.total + (self.producto.precio_contado * self.cantidad)
        self.producto.save() #Guardamos el producto dado que se modifico su stock
        self.venta.save() #Guardamos la venta junto a su detalle
        super(DetalleVenta, self).save() #Guardamos el detalle
    """
    def clean(self): # BEFORE INSERT OR UPDATE
        super(DetalleVenta, self).clean()
            if self.cantidad > self.producto.stock:
                raise ValidationError('Existencias insuficientes para realizar la venta')
    """

    def __str__ (self):
        cadena = "{0} {1} {2}"
        return cadena.format(self.venta, self.producto.nombre, self.cantidad)

    def Fecha (self):
        return str(self.venta.fecha)

    def Cliente (self):
        return self.venta.cliente

    def Vendedor(self):
        return self.venta.vendedor

    class Meta :
        db_table = 'detalle_ventacontado'
        verbose_name = 'Detalle de la venta al contado'
        verbose_name_plural = 'Detalles de las ventas al contado'
