from django.db import models
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

# Importaciones desde los modulos existentes
from Clientes.models import *
from Vendedores.models import *
from Productos.models import *


# Cración de la clase para las ventas al contado
class VentaContado(models.Model):
    fecha = models.DateField('Fecha', auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        cadena = "Venta No. {0}"
        return cadena.format(self.pk)

    def Total(self):
        return 'Q. %s' % self.total

    def agregarTotal(self, total):
        self.total += total

    def descontarTotal(self, total):
        self.total -= total

    # def getSaldo(self):
    #     from Cobros.models import Cobros
    #     try:
    #         ultimo_pago = Cobros.objects.filter(venta_id=self.pk).last()
    #         return ultimo_pago.saldo
    #     except:
    #         return self.saldo
    # getSaldo.short_description = 'Saldo Actual'

    # def save(self, **kwargs):
    #     """
    #     id_venta = self.pk
    #     item = DetalleVenta.objects.filter(venta_id=id_venta)
    #     total = 0
    #     for detalle in item:
    #         total += detalle.producto.precio_contado * detalle.cantidad
    #     self.total = total
    #     """
    #     super(VentaContado, self).save()

    def save(self, **kwargs):
        detalle = DetalleVenta.objects.filter(venta_id=self.pk)  # Instancear los detalles de la venta
        total = 0
        for d in detalle:  # Iterrar los detalles de una venta
            total += d.subtotal  # Calcular total de la venta
        self.total = total  # Agregar saldo calculado a la venta
        super(VentaContado, self).save()  # Guardamos la venta

    def Nit(self):
        return self.cliente.nit

    def ID(self):
        return self.id

    def Ventas(self):
        return mark_safe(u'<a href="/ventas" target="_blank">Ventas</a>')

    Ventas.short_description = 'Ventas'

    def comprobante(self):
        # retorna el link que abrira cuando se de un click y el nombre que tendra en la columna
        return mark_safe(u'<a href="/comprobante/?id=%s" target="_blank">Generar</a>' % self.id)
    comprobante.short_description = 'Comprobante'

    class Meta:
        db_table = 'venta_contado'
        verbose_name = 'Venta al contado'
        verbose_name_plural = 'Ventas al contado'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(VentaContado, on_delete=models.CASCADE, verbose_name='Venta')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.PositiveIntegerField(help_text='Solo ingresar números enteros positivos')
    subtotal = models.PositiveIntegerField(default=0)

    '''Función para capturar el total de la venta y poder modificarlo
        El total nos servirá para  
    '''

    # def save(self, **kwargs):
    #     total = self.venta.total
    #     id_producto = self.producto.pk
    #     id_venta = self.venta.pk
    #     if total == 0 : # Cuando no hay productos en la venta
    #         self.producto.descontarStock(self.cantidad)
    #         self.venta.total = self.venta.total + (self.producto.precio_contado * self.cantidad)
    #     else:
    #         try:
    #             item = DetalleVenta.objects.get(venta=id_venta, producto=id_producto)
    #             if item.cantidad > self.cantidad:
    #                 diferencia = item.cantidad - self.cantidad
    #                 self.producto.agregarStock(diferencia)
    #                 total=self.producto.precio_contado * self.cantidad
    #                 self.venta.descontarTotal(total)
    #             else:
    #                 diferencia = self.cantidad - item.cantidad
    #                 self.producto.descontarStock(diferencia)
    #                 total=self.producto.precio_contado * diferencia
    #                 self.venta.agregarTotal(total)
    #         except:
    #             self.producto.descontarStock(self.cantidad)
    #             self.venta.total = self.venta.total + (self.producto.precio_contado * self.cantidad)
    #
    #     self.producto.save() #Guardamos el producto dado que se modifico su stock
    #     self.venta.save() #Guardamos la venta junto a su detalle
    #     super(DetalleVenta, self).save() #Guardamos el detalle

    def save(self, *args, **kwargs):
        if self.venta.total == 0:  # si no hay productos agregados a la venta
            self.producto.descontarExistencias(self.cantidad)
        else:  # cuando ya hay productos agregados a la venta
            try:  # Detectar modificaciones en los productos ya registrados
                item = DetalleVenta.objects.get(venta=self.venta.pk, producto=self.producto.pk)
                if item.cantidad > self.cantidad:  # Detectar si la cantidad vendida es mayor o menor a la que se vendió anteriormente
                    diferencia = item.cantidad - self.cantidad  # Calcular la diferencia entre las cantidad
                    self.producto.agregarExistencias(diferencia)  # Regresar a las existencias las cantidad sobrantes
                else:  # En caso de que la cantidad vendida era menor a la que se requeria
                    diferencia = self.cantidad - item.cantidad  # Calcular la diferencia entre las cantidad
                    self.producto.descontarExistencias(
                        diferencia)  # Descontar de las existencias la cantidad extra vendida
            except:  # Cuando se agrega otro producto a la venta
                self.producto.descontarExistencias(self.cantidad)  # Descontar las existencias vendidas
        self.subtotal = self.producto.precio_contado * self.cantidad  # Agregar el subtotal al detalle
        super(DetalleVenta, self).save()  # Guardamos el detalle
        self.venta.save()  # Guardar los cambios en la venta para cada detalle

    # Acción que evita que la venta se realice con una cantidad de producto en decimales
    # y si excede las exitencias actuales
    def clean(self):
        super(DetalleVenta, self).clean()
        try:
            cantidad = int(self.cantidad)
            if cantidad > self.producto.existencias:
                raise ValidationError('Existencias insuficientes para realizar la venta Existencia actuales: '
                                      + str(self.producto.existencias))
        except:
            raise ValidationError('La cantidad ingresada no es entero.')

    def __str__(self):
        cadena = "{0}, Q. {1}.00"
        return cadena.format(self.producto.nombre, self.producto.precio_contado)

    def Fecha(self):
        return str(self.venta.fecha)

    def Cliente(self):
        return mark_safe('<span style="color: red">{0}</span>'.format(self.venta.cliente))

    def Vendedor(self):
        return self.venta.vendedor

    def Producto(self):
        return self.producto.nombre

    def Venta(self):
        return self.venta.pk

    class Meta:
        db_table = 'detalle_ventacontado'
        verbose_name = 'Detalle de la venta al contado'
        verbose_name_plural = 'Detalles de las ventas al contado'


class Informes(models.Model):
    meses = (
    ('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'),
    ('8', 'Agosto'), ('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'))
    fecha = models.DateField('Fecha', auto_now_add=True)
    fecha_inicio = models.DateField('Fecha de inicio', help_text='Fecha donde iniciará la búsqueda')
    fecha_fin = models.DateField('Fecha de fin', help_text='Fecha donde se finalizará la búsqueda')
    mes = models.CharField('Mes', max_length=2, choices=meses, default='1',
                           help_text='Mes que corresponde al informe a generar')

    def __str__(self):
        return str(self.fecha)

    def informe(self):
        # retorna el link que abrira cuando se de un click y el nombre que tendra en la columna
        return mark_safe(u'<a href="/informecontado/?id=%s" target="_blank">Informe</a>' % self.id)

    informe.short_description = 'Informe de Ventas al Contado'

    class Meta:
        db_table = 'informe_mensual_contado'
        verbose_name = 'Informe mensual, trimestral, anual'
        verbose_name_plural = 'Informes mensuales, trimestrales, anuales'
