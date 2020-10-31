from django.db import models
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta

#Importaciones desde los modulos existentes
from Clientes.models import *
from Vendedores.models import *
from Productos.models import *
#from Cobros.models import Cobros

#Cración de la clase para las ventas al contado
class VentaCredito(models.Model):
    tipos_pagos = (('1', 'Dos pagos'), ('2', 'Tres pagos'), ('3', 'Plazos'))
    fecha = models.DateField('Fecha') #auto_now_add = True
    cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete = models.CASCADE)
    credito = models.CharField('Crédito a', max_length=1, choices=tipos_pagos, default='1')
    total = models.PositiveIntegerField('Total', default=0)
    saldo = models.PositiveIntegerField('Saldo', default=0)
    enganche = models.PositiveIntegerField('Enganche', default=0, help_text = 'Ingresar solo números enteros')

    def __str__(self):
        cadena = "Venta No. {0}"
        return cadena.format(self.pk)

    def Total (self):
        return 'Q. %s.00' % self.total

    def Saldo (self):
        return 'Q. %s' % self.saldo

    def agregarTotal (self, total):
        self.total += total

    def descontarTotal (self, total):
        self.total -= total

    def agregarSaldo (self, saldo):
        self.saldo += saldo

    def descontarSaldo (self, saldo):
        self.saldo = self.saldo - saldo

    def setSaldo(self, monto):
        self.saldo=monto
        super(VentaCredito, self).save() #Guardamos la venta

    def cuotas_registradas(self):
        return mark_safe(u'<a href="/cuotas_registradas/?id=%s" target="_blank">Generar</a>' % self.id)
    cuotas_registradas.short_description = 'Cuotas'

    def Ventas (self):
        return mark_safe(u'<a href="/ventas" target="_blank">Ventas</a>')
    Ventas.short_description = 'Ventas'

    def getSaldo(self):
        saldo = 'Q. {}.00'
        from Cobros.models import Cobros
        try:
            ultimo_pago = Cobros.objects.filter(venta_id=self.pk).last()
            return saldo.format(ultimo_pago.saldo)
        except:
            return saldo.format(self.saldo)
    getSaldo.short_description = 'Saldo Actual'

    def comprobantecredito(self):
        #retorna el link que abrira cuando se de un click y el nombre que tendra en la columna
        return mark_safe(u'<a href="/comprobantecredito/?id=%s" target="_blank">Generar</a>' % self.id)
    comprobantecredito.short_description = 'Comprobante'



    # def save(self, **kwargs):
    #     #from Cobros.models import Cobros
    #     #ultima_cuota = Cobros.objects.filter(venta_id=self.pk).last()
    #     try:
    #         venta = VentaCredito.objects.get(id=self.pk)
    #         saldo_anterior = venta.saldo
    #         print("saldo anterior = " + str(saldo_anterior))
    #         print("saldo actual = " + str(self.saldo))
    #         print("total anterior =" + str(venta.total))
    #         print("total  actual = " + str(self.total))
    #         if saldo_anterior == self.total:
    #             print("Entro al if principal")
    #             self.saldo = self.total - self.enganche
    #             super(VentaCredito, self).save()
    #         elif saldo_anterior > 0:
    #             print("Entro al if de las cuotas")
    #             super(VentaCredito, self).save()
    #         elif self.total > 0 and self.saldo == 0:
    #             print("Entro al if de agregar saldo")
    #             self.saldo = self.total
    #             super(VentaCredito, self).save()
    #     except VentaCredito.DoesNotExist:
    #         self.saldo = self.total - self.enganche
    #         super(VentaCredito, self).save()
    #     super(VentaCredito, self).save()

    def save(self, **kwargs):
        detalle = DetalleVentaCredito.objects.filter(venta_id=self.pk) # Instancear los detalles de la venta
        total = 0
        for d in detalle: # Iterrar los detalles de una venta
            print('Entro al for')
            total += d.subtotal # Calcular total de la venta
        print('total calculado'+str(total))
        self.total = total # Agregar saldo calculado a la venta
        super(VentaCredito, self).save() #Guardamos la venta
        self.setSaldo(self.total) # Después de calcular el total, agregarmos el saldo a la venta
        if self.enganche > 0: # Procesar el saldo
            self.saldo = self.total - self.enganche # Descontar el enganche al saldo de la venta
            super(VentaCredito, self).save() #Guardamos la venta


    def clean(self): # Acción que evita que la venta se realice con una cantidad de producto en decimales y si excede las exitencias actuales
        super(VentaCredito, self).clean()
        if self.enganche > 0 and self.saldo == 0:
            raise ValidationError('Guardar venta antes de ingresar un enganche, dejar enganche a cero')

    def Nit (self):
        return self.cliente.nit

    def ID (self):
        return self.id

    def Cliente (self):
        from Cobros.models import Cobros
        cuotas_venta = Cobros.objects.filter(venta_id=self.pk).count()
        if cuotas_venta == 0: # Cuando no hay cuotas sobre la venta
            fecha_pago = self.fecha + timedelta(days=30)
            if fecha_pago < datetime.now().date():
                return mark_safe('<span style="color: red">{0}</span>'.format(self.cliente))
            else:
                return mark_safe('<span style="color: green">{0}</span>'.format(self.cliente))
        else:
            ultima_cuota = Cobros.objects.filter(venta_id=self.pk).last()
            if ultima_cuota.fecha.day == 31:
                fecha = ultima_cuota.fecha - timedelta(days=3)
                fecha_pago = fecha + timedelta(days=30)
            if ultima_cuota.fecha.day  == 30:
                fecha = ultima_cuota.fecha - timedelta(days=2)
                fecha_pago = fecha + timedelta(days=30)
            if ultima_cuota.fecha.day == 29:
                fecha = ultima_cuota.fecha - timedelta(days=1)
                fecha_pago = fecha + timedelta(days=30)
            if ultima_cuota.fecha.day <= 28:
                fecha_pago = ultima_cuota.fecha + timedelta(days=30)
            if fecha_pago < datetime.now().date():
                return mark_safe('<span style="color: red">{0}</span>'.format(self.cliente))
            elif fecha_pago == datetime.now().date():
                return mark_safe('<span style="color: green">{0}</span>'.format(self.cliente))
            else:
                return mark_safe('<span style="color: green">{0}</span>'.format(self.cliente))
    """
        id_venta = self.pk
        from Cobros.models import Cobros
        try:
            cuotas = Cobros.objects.filter(venta_id=id_venta).last()
            for x in cuotas:
                fecha_cuota = x.fecha
            if self.fecha.day > datetime.now().date().day:
                return mark_safe('<span style="color: red">{0}</span>'.format(self.cliente))
            if self.fecha.day < datetime.now().date().day:
                return mark_safe('<span style="color: GoldenRod">{0}</span>'.format(self.cliente))
        except:
            return mark_safe('<span style="color: green">{0}</span>'.format(self.cliente))
        """


    def getFecha (self):
        return self.fecha

    def FechaPago (self):
        """if self.fecha.month == 1 & self.fecha.day > 28:
            fechapago = self.fecha + timedelta(days=28)
            return fechapago
        else:
            fechapago = self.fecha + timedelta(days=30)
        #fechapago = '{0} de cada mes'
        #return fechapago.format(self.fecha.day)
            return fechapago"""
        if self.fecha.day == 31:
            dia = self.fecha - timedelta(days=3)
            fecha = '{0} de cada mes'
            return fecha.format(dia.day)
        if self.fecha.day == 30:
            dia = self.fecha - timedelta(days=2)
            fecha = '{0} de cada mes'
            return fecha.format(dia.day)
        if self.fecha.day == 29:
            dia = self.fecha - timedelta(days=1)
            fecha = '{0} de cada mes'
            return fecha.format(dia.day)
        if self.fecha.day <= 28:
            fecha = '{0} de cada mes'
            return fecha.format(self.fecha.day)

    class Meta :
        db_table = 'venta_credito'
        verbose_name = 'Venta al crédito'
        verbose_name_plural = 'Ventas al crédito'

class DetalleVentaCredito(models.Model):
    venta = models.ForeignKey(VentaCredito, on_delete=models.CASCADE, verbose_name = 'Venta')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name = 'Producto')
    cantidad = models.PositiveIntegerField(help_text='Solo enteros positivos')
    subtotal = models.PositiveIntegerField(default=0)

    '''Función para capturar el total de la venta y poder modificarlo
        El total nos servirá para  
    '''
    # def save(self, **kwargs):
    #     total = self.venta.total
    #     id_producto = self.producto.pk
    #     id_venta = self.venta.pk
    #     if total == 0 :
    #         if self.venta.credito == '1':
    #             self.venta.total = self.venta.total + (self.producto.precio_2pagos * self.cantidad)
    #             #self.venta.saldo =self.venta.total - int(self.engache)
    #             self.producto.descontarStock(self.cantidad)
    #         if self.venta.credito == '2':
    #             self.venta.total = self.venta.total + (self.producto.precio_3pagos * self.cantidad)
    #             #self.venta.saldo =self.venta.total - int(self.engache)
    #             self.producto.descontarStock(self.cantidad)
    #         if self.venta.credito == '3':
    #             self.venta.total = self.venta.total + (self.producto.precio_plazos * self.cantidad)
    #             #self.venta.saldo =self.venta.total - int(self.engache)
    #             self.producto.descontarStock(self.cantidad)
    #     else:
    #         try:
    #             item = DetalleVentaCredito.objects.get(venta=id_venta, producto=id_producto)
    #             """
    #             if item.cantidad == self.cantidad:
    #                 print('Entro al if de la cantidad')
    #                 if self.engache < item.engache:
    #                     print('Entro al if del enganche que va es menor al que habia')
    #                     print('Saldo que habia: '+str(self.venta.saldo))
    #                     saldo=item.engache - self.engache
    #                     print('Diferencia de engaches es '+str(saldo))
    #                     self.venta.agregarSaldo(saldo)
    #                 else:
    #                     print('Entro al if del enganche que va es mayor al que habia')
    #                     print('Saldo que habia: '+str(self.venta.saldo))
    #                     saldo=self.engache - item.engache
    #                     print('Diferencia de engaches es '+str(saldo))
    #                     self.venta.descontarSaldo(saldo)
    #             """
    #             if item.cantidad > self.cantidad:
    #                 diferencia = item.cantidad - self.cantidad
    #                 if self.venta.credito == '1':
    #                     self.producto.agregarStock(diferencia)
    #                     total=self.producto.precio_2pagos * self.cantidad
    #                     self.venta.descontarTotal(total)
    #                     self.venta.descontarSaldo(total)
    #                     #saldo=item.engache - int(self.engache)
    #                     #self.venta.agregarSaldo(saldo)
    #                 if self.venta.credito == '2':
    #                     self.producto.agregarStock(diferencia)
    #                     total=self.producto.precio_3pagos * self.cantidad
    #                     self.venta.descontarTotal(total)
    #                     self.venta.descontarSaldo(total)
    #                     #saldo=item.engache - int(self.engache)
    #                     #self.venta.agregarSaldo(saldo)
    #                 if self.venta.credito == '3':
    #                     self.producto.agregarStock(diferencia)
    #                     total=self.producto.precio_plazos * self.cantidad
    #                     self.venta.descontarTotal(total)
    #                     self.venta.descontarSaldo(total)
    #                     #saldo=item.engache - int(self.engache)
    #                     #self.venta.agregarSaldo(saldo)
    #             else:
    #                 diferencia = self.cantidad - item.cantidad
    #                 if self.venta.credito == '1':
    #                     self.producto.descontarStock(diferencia)
    #                     total=self.producto.precio_2pagos * diferencia
    #                     self.venta.agregarTotal(total)
    #                     self.venta.agregarSaldo(total)
    #                     #saldo=int(self.engache) - item.engache
    #                     #self.venta.descontarSaldo(saldo)
    #                 if self.venta.credito == '2':
    #                     self.producto.descontarStock(diferencia)
    #                     total=self.producto.precio_3pagos * diferencia
    #                     self.venta.agregarTotal(total)
    #                     self.venta.agregarSaldo(total)
    #                     #saldo=int(self.engache) - item.engache
    #                     #self.venta.descontarSaldo(saldo)
    #                 if self.venta.credito == '3':
    #                     self.producto.descontarStock(diferencia)
    #                     total=self.producto.precio_plazos * diferencia
    #                     self.venta.agregarTotal(total)
    #                     self.venta.agregarSaldo(total)
    #                     #saldo=int(self.engache) - item.engache
    #                     #self.venta.descontarSaldo(saldo)
    #         except:
    #             if self.venta.credito == '1':
    #                 self.producto.descontarStock(self.cantidad)
    #                 self.venta.total = self.venta.total + (self.producto.precio_2pagos * self.cantidad)
    #                 saldo = self.producto.precio_2pagos * self.cantidad
    #                 self.venta.agregarSaldo(saldo)
    #                 #saldo = (self.producto.precio_2pagos * self.cantidad)-int(self.engache)
    #                 #self.venta.agregarSaldo(saldo)
    #             if self.venta.credito == '2':
    #                 self.producto.descontarStock(self.cantidad)
    #                 self.venta.total = self.venta.total + (self.producto.precio_3pagos * self.cantidad)
    #                 saldo = self.producto.precio_3pagos * self.cantidad
    #                 self.venta.agregarSaldo(saldo)
    #                 #saldo = (self.producto.precio_3pagos * self.cantidad)-int(self.engache)
    #                 #self.venta.agregarSaldo(saldo)
    #             if self.venta.credito == '3':
    #                 self.producto.descontarStock(self.cantidad)
    #                 self.venta.total = self.venta.total + (self.producto.precio_plazos * self.cantidad)
    #                 saldo = self.producto.precio_plazos * self.cantidad
    #                 self.venta.agregarSaldo(saldo)
    #                 #saldo = (self.producto.precio_plazos * self.cantidad)-int(self.engache)
    #                 #self.venta.agregarSaldo(saldo)
    #
    #     self.producto.save()
    #     self.venta.save() #Guardamos la venta junto a su detalle
    #     super(DetalleVentaCredito, self).save() #Guardamos el detalle

    def save(self, *args, **kwargs):
        print('Entro al save del detalle')
        if self.venta.credito == '1':
            print('Entro al if de dos pagos')
            self.subtotal = self.producto.precio_2pagos * self.cantidad # Agregar el subtotal al detalle
            super(DetalleVentaCredito, self).save() #Guardamos el detalle
        if self.venta.credito == '2':
            self.subtotal = self.producto.precio_3pagos * self.cantidad # Agregar el subtotal al detalle
            super(DetalleVentaCredito, self).save() #Guardamos el detalle
        if self.venta.credito == '3':
            self.subtotal = self.producto.precio_plazos * self.cantidad # Agregar el subtotal al detalle
            super(DetalleVentaCredito, self).save() #Guardamos el detalle
        # Manejo de existencias
        if self.venta.total == 0: # si no hay productos agregas a la venta
            self.producto.descontarExistencias(self.cantidad)
        else: # cuando ya hay productos agregados a la venta
            try: # Detectar modificaciones en los productos ya registrados
                item = DetalleVentaCredito.objects.get(venta=self.venta.pk, producto=self.producto.pk)
                if item.cantidad > self.cantidad: # Detectar si la cantidad vendida es mayor o menor a la que se vendió anteriormente
                    diferencia = item.cantidad - self.cantidad # Calcular la diferencia entre las cantidad
                    self.producto.agregarExistencias(diferencia) # Regresar a las existencias las cantidad sobrantes
                else: # En caso de que la cantidad vendida era menor a la que se requeria
                    diferencia = self.cantidad - item.cantidad # Calcular la diferencia entre las cantidad
                    self.producto.descontarExistencias(diferencia) # Descontar de las existencias la cantidad extra vendida
            except: # Cuando se agrega otro producto a la venta
                self.producto.descontarExistencias(self.cantidad) # Descontar las existencias vendidas
        # Calcular Subtotal
        super(DetalleVentaCredito, self).save() #Guardamos el detalle
        self.venta.save() # Guardar los cambios en la venta para cada detalle

    def clean(self): # Acción que evita que la venta se realice con una cantidad de producto en decimales y si excede las exitencias actuales
        super(DetalleVentaCredito, self).clean()
        try:
            cantidad = int(self.cantidad)
            if cantidad > self.producto.existencias:
                raise ValidationError('Existencias insuficientes para realizar la venta. Existencia actuales: '+str(self.producto.existencias))
        except:
            raise ValidationError('La cantidad ingresada no es entero')

    def __str__ (self):
        cadena = "{0}, Q. {1}.00"
        if self.venta.credito == '1':
            return cadena.format(self.producto.nombre, self.producto.precio_2pagos)
        if self.venta.credito == '2':
            return cadena.format(self.producto.nombre, self.producto.precio_3pagos)
        if self.venta.credito == '3':
            return cadena.format(self.producto.nombre, self.producto.precio_plazos)

    def Fecha (self):
        return str(self.venta.fecha)

    def Cliente (self):
        return self.venta.cliente

    def Vendedor(self):
        return self.venta.vendedor

    def Producto (self):
        return self.producto.nombre

    def Venta (self):
        return self.venta.pk

    class Meta :
        db_table = 'detalle_ventacredito'
        verbose_name = 'Detalle de la venta al crédito'
        verbose_name_plural = 'Detalles de las ventas al crédito'

class Referencia (models.Model):
    opciones_relacion = (('A', 'Personal'),('F', 'Familiar'),('L', 'Laboral'),)
    venta = models.ForeignKey(VentaCredito, on_delete = models.CASCADE, verbose_name = 'Venta')
    nombre = models.CharField('Nombre completo', max_length=100)
    relacion = models.CharField('Relación con el Cliente', max_length=1, choices=opciones_relacion, default='F')
    numero = models.PositiveIntegerField ('Número de Teléfono', help_text='Solo ingresar números')

    def __str__(self):
        cadena = "{0} {1} {2} "
        return cadena.format(self.relacion, self.nombre, self.numero)

    def Cliente (self):
        return self.venta.cliente

    class Meta:
        db_table = 'referencia'
        verbose_name = 'Referencia'
        verbose_name_plural = 'Referencias'

class Informes (models.Model):
    meses = (('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'))
    fecha = models.DateField('Fecha', auto_now_add = True)
    fecha_inicio = models.DateField('Fecha de inicio', help_text='Fecha donde iniciará la búsqueda')
    fecha_fin = models.DateField('Fecha de fin', help_text='Fecha donde se finalizará la búsqueda')
    mes = models.CharField('Mes', max_length=2, choices=meses, default='1', help_text='Mes que corresponde al informe a generar')

    def __str__(self):
        return str(self.fecha)

    def informe(self):
        #retorna el link que abrira cuando se de un click y el nombre que tendra en la columna
        return mark_safe(u'<a href="/informemensual/?id=%s" target="_blank">Informe</a>' % self.id)
    informe.short_description = 'Informe de Ventas al Crédito'

    class Meta:
        db_table = 'informe_mensual_credito'
        verbose_name = 'Informe mensual, trimestral, anual'
        verbose_name_plural = 'Informes mensuales, trimestrales, anuales'
