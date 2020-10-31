from django.contrib import admin
from .models import *

# Register your models here.

class VentaDetalleContado (admin.TabularInline):
    model = DetalleVenta
    extra = 0
    min_num = 1
    max_num = 10
    autocomplete_fields = ['producto']
    readonly_fields = ['subtotal']

class VentaContadoAdmin (admin.ModelAdmin):
    inlines = [VentaDetalleContado]
    readonly_fields = ['total']
    search_fields = ['cliente__nombres', 'cliente__apellidos', 'cliente__nit']
    list_filter = ['fecha', 'vendedor']
    date_hierarchy="fecha"
    list_display = ['id','fecha', 'cliente', 'vendedor','Total', 'comprobante']
    list_per_page = 15
    ordering = ['fecha']
    autocomplete_fields = ['cliente', 'vendedor']

class DetalleVentaAdmin (admin.ModelAdmin):
    readonly_fields = ['subtotal']
    search_fields = ['producto__nombre','venta__cliente__nombres']
    list_filter = ['producto__tipo','venta__fecha']
    list_display = ['Venta', 'Fecha', 'Producto', 'cantidad']
    ordering = ['venta__fecha']
    autocomplete_fields = ['producto','venta']

class InformesAdmin (admin.ModelAdmin):
    search_fields = ['fecha']
    list_filter = ['fecha']
    list_display = ['fecha', 'mes', 'informe']
    ordering = ['fecha']

admin.site.register(VentaContado, VentaContadoAdmin)
admin.site.register(DetalleVenta, DetalleVentaAdmin)
admin.site.register(Informes, InformesAdmin)
