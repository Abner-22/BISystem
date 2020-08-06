#Importaciones desde django
from django.contrib import admin

#Importaciones desde los modelos de Municipio
from Municipio.models import *

class DepartamentoAdmin(admin.ModelAdmin):
    search_fields = ['nombre'] #Permite realizar búsquedas tomando como parámeto el atributo nombre
    list_display = ['nombre'] #Muestra en pantalla el atributo nombre del departamento
    ordering = ['nombre']

class MunicipioAdmin(admin.ModelAdmin):
    search_fields = ['nombre'] #Permite realizar búsquedas tomando como parámeto el atributo nombre
    list_filter = ['departamento'] #Crear un filtro para realizar búsquedas por departamento
    list_display = ['nombre', 'departamento'] #Muestra en pantalla los atributos nombre y departamento del cada municipio.
    ordering = ['nombre']
    autocomplete_fields = ['departamento',]

admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Municipio, MunicipioAdmin)
