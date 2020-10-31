from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from Ventas_Credito.models import VentaCredito, DetalleVentaCredito, Informes
from Cobros.models import Cobros
# Create your views here.

class VentasCreditoPDFView(PDFTemplateView):
    #archivo donde se va a desplegar la info , hay una carpeta llamada templates
    template_name = "ventascredito.html"

    def get_context_data(self, **kwargs):
        #se hace una instancia del objeto a iterar
        sales = VentaCredito.objects.all().order_by("id")

        #parametros de salida del reporte,
        return super(VentasCreditoPDFView, self).get_context_data(
            pagesize="Letter landscape",
            titulo="VentasCredito",
            ventas=sales,
            **kwargs
        )
class VentaCreditoPDFView(PDFTemplateView):
    template_name = "comprobantecredito.html"

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get("id")
        sale = VentaCredito.objects.get(id=ids)
        saledetail = DetalleVentaCredito.objects.filter(venta=ids)

        return super(VentaCreditoPDFView, self).get_context_data(
            pagesize="Letter",
            titulo="Comprobantecredito",
            venta=sale,
            detalle=saledetail,
            **kwargs
        )

class InformeMensualPDFView(PDFTemplateView):
    template_name = "informe_mensual.html"

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get("id")
        informe = Informes.objects.get(id=ids)
        fecha_inicio = informe.fecha_inicio
        fecha_fin = informe.fecha_fin
        month = fecha_inicio.month
        year = fecha_inicio.year
        sales = VentaCredito.objects.filter(fecha__range=(fecha_inicio, fecha_fin))

        return super(InformeMensualPDFView, self).get_context_data(
            pagesize="Letter landscape",
            titulo="InformeMensual",
            ventas=sales,
            mes=month,
            año=year,
            **kwargs
        )

class VentaCreditoCuotasPDFView(PDFTemplateView):
    template_name = "cuotas_registradas.html"

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get("id")
        sale = VentaCredito.objects.get(id=ids)
        quota = Cobros.objects.filter(venta=ids).order_by("id")

        return super(VentaCreditoCuotasPDFView, self).get_context_data(
            pagesize="Letter",
            titulo="cuotas",
            venta=sale,
            cuotas=quota,
            **kwargs
        )
