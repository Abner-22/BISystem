"""BISystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.urls import path
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from Productos.views import InventoryPDFView, ProductosMas, VentasCount
from Clientes.views import ClientesPDFView
from Ventas_Contado.views import VentasContadoPDFView, VentaContadoPDFView, InformeContadoPDFView
from Ventas_Credito.views import VentasCreditoPDFView, VentaCreditoPDFView, InformeMensualPDFView, VentaCreditoCuotasPDFView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tablero/', VentasCount.as_view(), name="tablero"),
    url(r"^inventario/", InventoryPDFView.as_view(), name = "inventario"),
    url(r"^clientes/", ClientesPDFView.as_view(), name = "clientes"),
    url(r"^ventascontado/", VentasContadoPDFView.as_view(), name = "ventascontado"),
    url(r"^comprobante/", VentaContadoPDFView.as_view()),
    url(r"^ventascredito/", VentasCreditoPDFView.as_view(), name = "ventascredito"),
    url(r"^comprobantecredito/", VentaCreditoPDFView.as_view()),
    url(r"^cuotas_registradas/", VentaCreditoCuotasPDFView.as_view()),
    url(r"^informemensual/", InformeMensualPDFView.as_view(), name = "informemensual"),
    url(r"^informecontado/", InformeContadoPDFView.as_view(), name = "informecontado"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
