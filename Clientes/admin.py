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
    #search_fields = ['names', 'surnames', 'municipality','email', 'cui', 'nit']
    list_filter = ['genero', 'municipio__departamento', 'municipio','estado']
    fields = (('nombres', 'apellidos'), ('genero','fecha_nacimiento'), ('cui','nit'),('municipio','direccion'),'correo','estado')
    list_display = ['nombres', 'apellidos', 'edad', 'nit', 'Departamento', 'municipio','estado']
    ordering = ['nombres'] #visualizaremos los datos ordenados por nombres
    autocomplete_fields = ['municipio',]

class TelefonoAdmin (admin.ModelAdmin):
    search_fields = ['cliente__nombres','numero','tipo']
    list_filter = ['cliente__nombres','numero']
    list_display = ['cliente', 'numero', 'tipo']
    autocomplete_fields = ['cliente', 'tipo']

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(NumeroTelefonico)
