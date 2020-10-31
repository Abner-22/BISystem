from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from Ventas_Contado.models import VentaContado, DetalleVenta, Informes
# Create your views here.

class VentasContadoPDFView(PDFTemplateView):
    #archivo donde se va a desplegar la info , hay una carpeta llamada templates
    template_name = "ventas.html"

    def get_context_data(self, **kwargs):
        #se hace una instancia del objeto a iterar
        sales = VentaContado.objects.all()

        #parametros de salida del reporte,
        return super(VentasContadoPDFView, self).get_context_data(
            pagesize="Letter landscape",
            titulo="Ventas",
            ventas=sales,
            **kwargs
        )

class VentaContadoPDFView(PDFTemplateView):
    template_name = "comprobante.html"

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get("id")
        sale = VentaContado.objects.get(id=ids)
        saledetail = DetalleVenta.objects.filter(venta=ids)

        return super(VentaContadoPDFView, self).get_context_data(
            pagesize="Letter",
            titulo="Comprobante",
            venta=sale,
            detalle=saledetail,
            **kwargs
        )

class InformeContadoPDFView(PDFTemplateView):
    template_name = "informe_vario.html"

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get("id")
        informe = Informes.objects.get(id=ids)
        fecha_inicio = informe.fecha_inicio
        fecha_fin = informe.fecha_fin
        month = fecha_inicio.month
        year = fecha_inicio.year
        sales = VentaContado.objects.filter(fecha__range=(fecha_inicio, fecha_fin))

        return super(InformeContadoPDFView, self).get_context_data(
            pagesize="Letter landscape",
            titulo="InformeVario",
            ventas=sales,
            mes=month,
            año=year,
            **kwargs
        )
