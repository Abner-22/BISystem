from django.contrib import admin

#Importaciones desde los modules existentes
from Productos.models import *

class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ['estado']
    search_fields = ['nombre','tipo', 'estado']
    list_filter = ['tipo']
    fields = (('tipo', 'nombre'), 'descripcion', ('precio_costo', 'precio_contado', 'precio_2pagos', 'precio_3pagos', 'precio_plazos'), 'existencias', 'estado')
    list_display = ['id', 'nombre', 'PrecioCosto', 'PrecioContado', 'Precio2Pagos', 'Precio3Pagos', 'PrecioPlazos', 'existencias','estado']
    ordering = ['nombre'] #visualizaremos los datos ordenados por nombres

class AgregarExistenciaAdmin(admin.ModelAdmin):
    search_fields = ['producto__nombre']
    list_filter = ['producto__tipo','producto__estado']
    fields = ['producto', 'cantidad']
    list_display = ['fecha', 'Producto', 'cantidad']
    ordering = ['fecha']
    autocomplete_fields = ['producto']

admin.site.register(Producto, ProductoAdmin)
admin.site.register(AgregarExistencia, AgregarExistenciaAdmin)
