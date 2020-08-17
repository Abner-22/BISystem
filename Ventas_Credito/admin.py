from django.contrib import admin
from Ventas_Credito.models import DetalleVentaCredito
from Referencias.models import *
# Register your models here.

class VentaDetalleCredito (admin.TabularInline):
    model = DetalleVentaCredito
    extra = 0
    min_num = 1
    max_num = 10
    autocomplete_fields = ['producto']

class ReferenciaCliente (admin.TabularInline):
    model = Referencia
    extra = 0
    min_num = 1
    max_num = 10
    autocomplete_fields = ['cliente', 'venta']

class VentaCreditoAdmin (admin.ModelAdmin):
    inlines = [VentaDetalleCredito, ReferenciaCliente]
    readonly_fields = ['total']
    search_fields = ['cliente__nombres', 'cliente__apellidos', 'cliente__nit']
    list_filter = ['fecha', 'vendedor']
    list_display = ['fecha', 'cliente', 'vendedor', 'credito','Total']
    ordering = ['fecha']
    autocomplete_fields = ['cliente', 'vendedor']

class DetalleVentaCreditoAdmin (admin.ModelAdmin):
    search_fields = ['producto__nombre','cliente__nombres']
    list_filter = ['producto__tipo','venta__fecha', 'venta__credito']
    list_display = ['Fecha', 'Cliente', 'Vendedor', 'producto','cantidad']
    ordering = ['venta__fecha']
    autocomplete_fields = ['producto','venta']

admin.site.register(VentaCredito, VentaCreditoAdmin)
admin.site.register(DetalleVentaCredito, DetalleVentaCreditoAdmin)
