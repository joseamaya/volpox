from django.shortcuts import render
from django.views.generic import TemplateView
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from localizacion.models import Provincia, Distrito, Region

class Tablero(TemplateView):
    template_name = "tablero_actas.html"        

class BusquedaProvincias(TemplateView):

    def get(self, request, *args, **kwargs):
        region = request.GET['region']
        provincias = Provincia.objects.filter(region=region)
        if provincias:
            data = serializers.serialize('json', provincias, fields= ('pk','nombre'))
        else:
            data = []
        return HttpResponse(data, content_type='application/json')

class BusquedaDistritos(TemplateView):

    def get(self, request, *args, **kwargs):
        provincia = request.GET['provincia']
        distritos = Distrito.objects.filter(provincia=provincia)
        if distritos:
            data = serializers.serialize('json', distritos, fields= ('id','nombre'))
        else:
            data = []
        return HttpResponse(data, content_type='application/json')

def seleccion_distrito(request):
    regiones = Region.objects.order_by('nombre')
    if request.method == 'POST':
        distrito = request.POST['distritos']
        return HttpResponseRedirect(reverse('regional:reporte_distrital', args=[distrito]))
    context = {'regiones':regiones}
    return render(request, 'seleccion_distrito.html', context)

def seleccion_prov_consejero(request):
    regiones = Region.objects.order_by('nombre')
    if request.method == 'POST':
        provincia = request.POST['provincias']
        return HttpResponseRedirect(reverse('regional:reporte_consejero_regional', args=[provincia]))
    context = {'regiones':regiones}
    return render(request, 'seleccion_consejero_prov.html', context)

def seleccion_provincia(request):
    regiones = Region.objects.order_by('nombre')
    if request.method == 'POST':
        provincia = request.POST['provincias']
        return HttpResponseRedirect(reverse('regional:reporte_provincial', args=[provincia]))
    context = {'regiones':regiones}
    return render(request, 'seleccion_provincia.html', context)

def seleccion_region(request):
    regiones = Region.objects.order_by('nombre')
    if request.method == 'POST':
        region = request.POST['regiones']
        return HttpResponseRedirect(reverse('nacional:reporte_congresal', args=[region]))
    context = {'regiones':regiones}
    return render(request, 'seleccion_region.html', context)