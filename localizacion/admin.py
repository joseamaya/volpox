from django.contrib import admin
from localizacion.models import Region, Provincia, Distrito, Partido, CentroVotacion

class ProvinciaAdmin(admin.ModelAdmin):
    ordering = ('nombre',)

class DistritoAdmin(admin.ModelAdmin):
    ordering = ('nombre',)

class CentroVotacionAdmin(admin.ModelAdmin):
    ordering = ('distrito','nombre',)    

admin.site.register(Region)
admin.site.register(Provincia,ProvinciaAdmin)
admin.site.register(Distrito, DistritoAdmin)
admin.site.register(Partido)
admin.site.register(CentroVotacion, CentroVotacionAdmin)