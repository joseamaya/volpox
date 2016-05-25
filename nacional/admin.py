from django.contrib import admin
from nacional.models import MesaNacional, DetalleDisenioActaPresidencial,\
    DisenioActaPresidencial, DetalleDisenioActaCongresal, DisenioActaCongresal

# Register your models here.
class DetalleDisenioActaNacionalEnLinea(admin.TabularInline):
    model = DetalleDisenioActaPresidencial

class DisenioActaPresidencialAdmin(admin.ModelAdmin):
    inlines = [DetalleDisenioActaNacionalEnLinea]

class DetalleDisenioActaCongresalEnLinea(admin.TabularInline):
    model = DetalleDisenioActaCongresal

class DisenioActaCongresalAdmin(admin.ModelAdmin):
    inlines = [DetalleDisenioActaCongresalEnLinea]

admin.site.register(MesaNacional)
admin.site.register(DisenioActaPresidencial, DisenioActaPresidencialAdmin)
admin.site.register(DisenioActaCongresal, DisenioActaCongresalAdmin)