from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.

class Producto (models.Model):
    opciones_tipo = (('A', 'Amueblado'), ('M', 'Mueble'), ('S', 'Silla'), )
    tipo = models.CharField('Tipo de producto', max_length = 1, choices = opciones_tipo,
                            default = 'S')
    nombre = models.CharField('Nombre del producto', max_length = 100)
    descripcion = models.TextField('Descripción del Producto', max_length = 250)
    precio_costo = models.PositiveIntegerField ('Precio al costo',
                                                help_text='Solo ingresar números enteros positivos')
    existencias = models.PositiveIntegerField ('Cantidad de existencias',
                                               help_text='Solo ingresar números enteros positivos')
    precio_contado = models.PositiveIntegerField ('Precio de contado',
                                                help_text='Solo ingresar números enteros positivos')
    precio_2pagos = models.PositiveIntegerField ('Precio para 2 pagos',
                                                 help_text='Solo ingresar números enteros positivos')
    precio_3pagos = models.PositiveIntegerField ('Precio para 3 pagos',
                                                 help_text='Solo ingresar números enteros positivos')
    precio_plazos = models.PositiveIntegerField ('Precio a plazos',
                                                 help_text='Solo ingresar números enteros positivos')
    estado = models.BooleanField('Estado', default=True)

    def __str__ (self) :
        return self.InformaciónProducto()

    def InformaciónProducto (self):
        cadena = '{0}, Contado:Q.{1}, Dos pagos: Q.{2}, Tres pagos: Q.{3}, Plazos: Q.{4}'
        return cadena.format(self.nombre, self.precio_contado, self.precio_2pagos,
                             self.precio_3pagos, self.precio_plazos)

    def Producto (self):
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

    def descontarExistencias(self, cantidad):
        self.existencias -= cantidad
        self.save()

    def agregarExistencias(self, cantidad):
        self.existencias += cantidad
        self.save()

    def masvendidocredito(self): #Mas vendido al crédito
        from Ventas_Credito.models import DetalleVentaCredito
        productos = Producto.objects.all() #obtener todos lo producto
        vendidos = {}
        for p in productos:
            id_producto = p.pk #almaceno el id del primer producto
            detalles = DetalleVentaCredito.objects.filter(producto_id=id_producto).count() #cuantas veces aparece ese producto en los detalles
            vendidos[str(p.nombre)]= detalles
        mayor = {}
        max = 0
        for clave, valor  in vendidos.items():
            if valor > max:
                key = clave
                valor = valor
                max = valor
        mayor[key] = valor
        return key

    def masvendidocontado(self): #Mas vendido al crédito
        from Ventas_Contado.models import DetalleVenta
        productos = Producto.objects.all() #obtener todos lo producto
        vendidos = {}
        for p in productos:
            id_producto = p.pk #almaceno el id del primer producto
            detalles = DetalleVenta.objects.filter(producto_id=id_producto).count() #cuantas veces aparece ese producto en los detalles
            vendidos[str(p.nombre)]= detalles
        mayor = {}
        max = 0
        for clave, valor  in vendidos.items():
            if valor > max:
                key = clave
                valor = valor
                max = valor
        mayor[key] = valor
        return key

    def menosvendidocredito(self): #Menos vendido al crédito
        from Ventas_Credito.models import DetalleVentaCredito
        productos = Producto.objects.all() #obtener todos lo producto
        vendidos = {}
        menor = 0
        for p in productos:
            id_producto = p.pk #almaceno el id del primer producto
            detalles = DetalleVentaCredito.objects.filter(producto_id=id_producto).count() #cuantas veces aparece ese producto en los detalles
            vendidos[str(p.nombre)]= detalles
            menor = detalles
            #print('menor: '+str(menor))
        mayor = {}
        for clave, valor  in vendidos.items():
            #print("Valor: "+str(valor))
            #print("Menor: "+str(menor))
            if valor <= menor:
                key = clave
                valor = valor
                menor = valor
        mayor[clave] = valor
        return key

    def menosvendidocontado(self): #Menos vendido al crédito
        from Ventas_Contado.models import DetalleVenta
        productos = Producto.objects.all() #obtener todos lo producto
        vendidos = {}
        menor = 0
        for p in productos:
            id_producto = p.pk #almaceno el id del primer producto
            detalles = DetalleVenta.objects.filter(producto_id=id_producto).count() #cuantas veces aparece ese producto en los detalles
            vendidos[str(p.nombre)]= detalles
            menor = detalles
            #print('menor: '+str(menor))
        mayor = {}
        for clave, valor  in vendidos.items():
            #print("Valor: "+str(valor))
            #print("Menor: "+str(menor))
            if valor <= menor:
                key = clave
                valor = valor
                menor = valor
        mayor[clave] = valor
        return key

    def Inventario(self):
        return mark_safe(u'<a href="/inventario" target="_blank">Inventario</a>')
    Inventario.short_description = 'Inventario'

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        unique_together = ['nombre']

class AgregarExistencia (models.Model):
    fecha = models.DateField(auto_now_add=True, verbose_name='Fecha de ingreso') #se agrega automaticamente la fecha actual
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name = 'Producto')
    cantidad = models.PositiveIntegerField('Cantidad que ingresó')

    def __str__(self):
        return str(self.fecha)

    def Producto (self):
        return self.producto.nombre

    def save(self, **kwargs):
        self.producto.agregarExistencias(self.cantidad)
        self.producto.save()
        super(AgregarExistencia, self).save()

    class Meta:
        db_table = 'agregar_existencia'
        verbose_name = 'Ingreso de existencias'
        verbose_name_plural = 'Ingresos de existencias'
