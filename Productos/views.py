from django.shortcuts import render
from datetime import datetime
from easy_pdf.views import PDFTemplateView
from Productos.models import Producto
from django.views.generic import TemplateView
from Ventas_Contado.models import VentaContado
from Ventas_Credito.models import VentaCredito
from django.db.models import Sum
# Create your views here.

class InventoryPDFView(PDFTemplateView):
    #archivo donde se va a desplegar la info , hay una carpeta llamada templates
    template_name = "inventario.html"

    def get_context_data(self, **kwargs):
        #se hace una instancia del objeto a iterar
        productos = Producto.objects.all()

        #parametros de salida del reporte,
        return super(InventoryPDFView, self).get_context_data(
            pagesize="Letter landscape",
            titulo="ventascontado",
            productos=productos,
            **kwargs
        )

class ProductosMas(TemplateView):
    template_name="productos/tablero.html"

    def get_context_data(self, *args, **kwargs):
        producto=Producto.objects.first()
        return {'producto1':producto}

class VentasCount(TemplateView):
    template_name="productos/tablero.html"

    def get_GraficaData(self):
        datos = []
        try:
            año = datetime.now().year
            for m in range(1, 13):
               cantidad = VentaContado.objects.filter(fecha__year=año, fecha__month=m).count()
               datos.append(int(cantidad))
        except:
            pass
        return datos

    def get_GraficaData2(self):
        datos = []
        try:
            año = datetime.now().year
            for m in range(1, 13):
               cantidad = VentaCredito.objects.filter(fecha__year=año, fecha__month=m).count()
               datos.append(int(cantidad))
        except:
            pass
        return datos

    def get_Total_Contado(self):
        datos = []
        try:
            año = datetime.now().year
            for m in range(1, 13):
               ventas = VentaContado.objects.filter(fecha__year=año, fecha__month=m)
               Total = 0
               for v in ventas:
                   Total += v.total
               datos.append(Total)
        except:
            pass
        return datos

    def get_Total_Credito(self):
        datos = []
        try:
            año = datetime.now().year
            for m in range(1, 13):
               ventas = VentaCredito.objects.filter(fecha__year=año, fecha__month=m)
               Total = 0
               for v in ventas:
                   Total += v.total
               datos.append(Total)
        except:
            pass
        return datos

    def get_Producto(self):
        producto=Producto.objects.first()
        return producto

    def get_Año(self):
        año = datetime.now().year
        return año

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grafica'] = self.get_GraficaData()
        context['producto1'] = self.get_Producto()
        context['grafica2'] = self.get_GraficaData2()
        context['año'] = self.get_Año()
        context['contado'] = self.get_Total_Contado()
        context['credito'] = self.get_Total_Credito()
        return context
"""
def productomasvendidocontado ():
    producto=Producto.objects.first()
    print(producto.masvendidocontado())
    return producto.masvendidocontado()
"""
