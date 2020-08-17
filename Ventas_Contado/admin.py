from django.contrib import admin
from .models import *

# Register your models here.

class VentaDetalleContado (admin.TabularInline):
    model = DetalleVenta
    extra = 0
    min_num = 1
    max_num = 10
    autocomplete_fields = ['producto']

class VentaContadoAdmin (admin.ModelAdmin):
    inlines = [VentaDetalleContado]
    readonly_fields = ['total']
    search_fields = ['cliente__nombres', 'cliente__apellidos', 'cliente__nit']
    list_filter = ['fecha', 'vendedor']
    list_display = ['fecha', 'cliente', 'vendedor','Total']
    ordering = ['fecha']
    autocomplete_fields = ['cliente', 'vendedor']

class DetalleVentaAdmin (admin.ModelAdmin):
    search_fields = ['producto__nombre','venta__cliente__nombres']
    list_filter = ['producto__tipo','venta__fecha']
    list_display = ['Fecha', 'Cliente', 'Vendedor', 'producto', 'cantidad']
    ordering = ['venta__fecha']
    autocomplete_fields = ['producto','venta']


admin.site.register(VentaContado, VentaContadoAdmin)
admin.site.register(DetalleVenta, DetalleVentaAdmin)
