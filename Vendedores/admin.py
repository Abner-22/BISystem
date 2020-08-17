from django.contrib import admin

#Importaciones desde los modulos creados
from Vendedores.models import *

class TelefonoVendedor (admin.TabularInline):
    model = NumeroTelefonico
    extra = 1
    max_num = 3

class VendedorAdmin(admin.ModelAdmin):
    inlines = [TelefonoVendedor]
    readonly_fields = ['estado']
    search_fields = ['nombres', 'apellidos']
    list_filter = ['genero', 'estado']
    fields = (('nombres', 'apellidos'), ('genero','fecha_nacimiento'), ('cui','codigo'),('municipio','direccion'),'correo','estado')
    list_display = ['nombres', 'apellidos', 'edad', 'codigo', 'Departamento', 'municipio','estado']
    ordering = ['nombres'] #visualizaremos los datos ordenados por nombres
    autocomplete_fields = ['municipio',]

class TelefonoAdmin (admin.ModelAdmin):
    search_fields = ['vendedor__nombres','numero','tipo']
    list_filter = ['tipo']
    list_display = ['vendedor', 'numero', 'tipo']
    autocomplete_fields = ['vendedor']

admin.site.register(Vendedor, VendedorAdmin)
admin.site.register(NumeroTelefonico, TelefonoAdmin)
