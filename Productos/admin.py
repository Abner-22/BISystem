from django.contrib import admin

#Importaciones desde los modules existentes
from Productos.models import *

class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ['estado']
    search_fields = ['tipo', 'estado']
    list_filter = ['nombre', 'tipo']
    fields = (('tipo', 'nombre'), 'descripcion', ('precio_costo', 'precio_contado', 'precio_2pagos', 'precio_3pagos', 'precio_plazos'), 'estado')
    list_display = ['nombre', 'tipo', 'PrecioCosto', 'PrecioContado', 'Precio2Pagos', 'Precio3Pagos', 'PrecioPlazos', 'estado']
    ordering = ['nombre'] #visualizaremos los datos ordenados por nombres

admin.site.register(Producto, ProductoAdmin)
