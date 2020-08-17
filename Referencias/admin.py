from django.contrib import admin

from Referencias.models import *
# Register your models here.

class ReferenciaAdmin (admin.ModelAdmin):
    search_fields = ['cliente__nombres','cliente__apellidos']
    list_filter = ['relacion']
    list_display = ['cliente', 'relacion', 'nombre', 'numero']
    ordering = ['cliente']
    autocomplete_fields = ['cliente','venta']

admin.site.register(Referencia, ReferenciaAdmin)
