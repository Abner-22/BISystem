from django.contrib import admin
from Ventas_Credito.models import VentaCredito, DetalleVentaCredito, Referencia, Informes
# Register your models here.

class VentaDetalleCredito (admin.TabularInline):
    model = DetalleVentaCredito
    extra = 0
    min_num = 1
    max_num = 10
    autocomplete_fields = ['producto']
    readonly_fields = ['subtotal']

class ReferenciaCliente (admin.TabularInline):
    model = Referencia
    extra = 0
    min_num = 1
    max_num = 10
    autocomplete_fields = ['venta']

class VentaCreditoAdmin (admin.ModelAdmin):
    inlines = [VentaDetalleCredito, ReferenciaCliente]
    readonly_fields = ['total','saldo']
    search_fields = ['cliente__nombres', 'cliente__apellidos', 'id']
    list_filter = ['fecha', 'vendedor']
    date_hierarchy="fecha"
    list_display = ['id','fecha', 'Cliente', 'credito','Total', 'getSaldo', 'FechaPago', 'comprobantecredito', 'cuotas_registradas']
    ordering = ['fecha']
    autocomplete_fields = ['cliente', 'vendedor']

    # def add_view(self, request, extra_context=None):
    #     #     extra_context = extra_context or {}
    #     #     return super().add_view(request)

class DetalleVentaCreditoAdmin (admin.ModelAdmin):
    readonly_fields = ['subtotal']
    search_fields = ['producto__nombre','cliente__nombres']
    list_filter = ['producto__tipo','venta__fecha', 'venta__credito']
    list_display = ['Venta', 'Fecha', 'Producto','cantidad']
    ordering = ['venta__fecha']
    autocomplete_fields = ['producto','venta']

class ReferenciaAdmin (admin.ModelAdmin):
    search_fields = ['venta__cliente__nombres','venta__cliente__apellidos']
    list_filter = ['relacion']
    list_display = ['Cliente', 'relacion', 'nombre', 'numero']
    list_per_page = 15
    ordering = ['id']
    autocomplete_fields = ['venta']

class InformesAdmin (admin.ModelAdmin):
    search_fields = ['fecha']
    list_filter = ['fecha']
    list_per_page = 15
    list_display = ['fecha', 'mes', 'informe']
    ordering = ['fecha']

admin.site.register(VentaCredito, VentaCreditoAdmin)
admin.site.register(DetalleVentaCredito, DetalleVentaCreditoAdmin)
admin.site.register(Referencia, ReferenciaAdmin)
admin.site.register(Informes, InformesAdmin)
