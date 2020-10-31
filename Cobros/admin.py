from django.contrib import admin

from Cobros.models import Cobros

# Register your models here.
class CobrosAdmin (admin.ModelAdmin):
    readonly_fields = ['saldo']
    search_fields = ['venta__id']
    list_filter = ['fecha']
    date_hierarchy="fecha"
    list_per_page = 15
    list_display = ['fecha', 'venta', 'cliente', 'vendedor', 'Cuota', 'Saldo']
    ordering = ['fecha']
    autocomplete_fields = ['vendedor', 'venta']

admin.site.register(Cobros, CobrosAdmin)
