from django.contrib import admin

#Importaciones desde los modulos creados
from Clientes.models import *

class TelefonoCliente (admin.TabularInline):
    model = NumeroTelefonico
    extra = 1
    max_num = 3

class ClienteAdmin(admin.ModelAdmin):
    inlines = [TelefonoCliente]
    readonly_fields = ['estado']
    search_fields = ['nombres', 'apellidos']
    list_filter = ['genero', 'municipio__departamento', 'municipio','estado']
    fields = (('nombres', 'apellidos'), ('genero','fecha_nacimiento'), ('cui','nit'),('municipio','direccion'),'correo','estado')
    list_display = ['nombres', 'apellidos', 'edad', 'nit', 'municipio','estado']
    ordering = ['nombres'] #visualizaremos los datos ordenados por nombres
    autocomplete_fields = ['municipio',]

class TelefonoAdmin (admin.ModelAdmin):
    search_fields = ['cliente__nombres', 'cliente__apellidos', 'numero','tipo']
    list_filter = ['tipo']
    list_display = ['cliente', 'tipo', 'numero']
    autocomplete_fields = ['cliente']

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(NumeroTelefonico, TelefonoAdmin)
