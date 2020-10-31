from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from Clientes.models import Cliente
# Create your views here.

class ClientesPDFView(PDFTemplateView):
    #archivo donde se va a desplegar la información que se enviará en el context_data
    template_name = "clientes.html"

    def get_context_data(self, **kwargs):
        #instancia o varible que almacena los datos de todos los clientes
        clients = Cliente.objects.all()

        #parámetros y valores enviados al archivo html
        return super(ClientesPDFView, self).get_context_data(
            pagesize="Letter landscape",
            titulo="Clientes",
            clientes=clients,
            **kwargs
        )
