from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from regional.models import Mesa, DisenioActaRegional,\
    DetalleDisenioActaRegional, ActaRegional, DetalleActaRegional,\
    VotacionPresidenteRegional, VotacionConsejeroRegional, DisenioActaMunicipal,\
    DetalleDisenioActaMunicipal, ActaMunicipal, DetalleActaMunicipal,\
    VotacionProvincial, VotacionDistrital
from regional.forms import FormularioMesa, FormularioActaRegional,\
    FormularioActaMunicipal
from django.views.generic.base import TemplateView
from localizacion.models import CentroVotacion, Distrito, Provincia
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
import csv
from django.db.models import Sum
# Create your views here.

class Tablero(TemplateView):
    template_name = "tablero_regional.html" 

class ProcesarMesaMunicipal(FormView):
    template_name = "mesa_municipal.html"
    form_class = FormularioMesa
    
    def get_context_data(self, **kwargs):
        mesas = Mesa.objects.filter(procesada_municipal=False)
        context = super(ProcesarMesaMunicipal, self).get_context_data(**kwargs)
        context['mesas'] = mesas
        return context
    
    def form_valid(self, form):
        data = form.cleaned_data
        mesa = data['mesas']
        try: 
            obj_mesa = Mesa.objects.get(pk=mesa)
            return HttpResponseRedirect(reverse('localizacion:acta_municipal', args=[mesa]))
        except Mesa.DoesNotExist:
            return HttpResponseRedirect(reverse('localizacion:mesa_municipal'))

class ProcesarMesaRegional(FormView):    
    template_name = "mesa_regional.html"
    form_class = FormularioMesa
    
    def get_context_data(self, **kwargs):
        mesas = Mesa.objects.filter(procesada_regional=False)
        context = super(ProcesarMesaRegional, self).get_context_data(**kwargs)
        context['mesas'] = mesas
        return context
    
    def form_valid(self, form):
        data = form.cleaned_data
        mesa = data['mesas']
        try: 
            obj_mesa = Mesa.objects.get(pk=mesa)
            return HttpResponseRedirect(reverse('localizacion:acta_regional', args=[mesa]))
        except Mesa.DoesNotExist:
            return HttpResponseRedirect(reverse('localizacion:mesa_regional'))   

class ProcesarActaRegional(FormView):
    template_name = "acta_regional.html"
    form_class = FormularioActaRegional
    
    def get(self, request, *args, **kwargs):
        self.numero = kwargs['numero']
        return super(ProcesarActaRegional, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        self.mesa = Mesa.objects.get(numero=self.numero)
        try:
            disenio_acta = DisenioActaRegional.objects.get(region=self.mesa.centro_votacion.distrito.provincia.region)
        except DisenioActaRegional.DoesNotExist:
            return HttpResponseRedirect(reverse('admin:login'))
        self.detalles = DetalleDisenioActaRegional.objects.filter(disenio_acta=disenio_acta).order_by('id')
        context = super(ProcesarActaRegional, self).get_context_data(**kwargs)
        context['mesa'] = self.mesa
        context['disenio_acta'] = disenio_acta
        context['detalles'] = self.detalles
        return context    
    
    def form_valid(self, form):
        data = form.cleaned_data
        votos_blancos_pres = data['voto_blanco_pres']
        votos_nulos_pres = data['voto_nulo_pres']
        votos_imp_pres = data['voto_impugnado_pres']
        votos_tot_pres = data['voto_total_pres']
        votos_blancos_cons = data['voto_blanco_cons']
        votos_nulos_cons = data['voto_nulo_cons']
        votos_imp_cons = data['voto_impugnado_cons']
        votos_tot_cons = data['voto_total_cons']
        acta = ActaRegional(mesa=self.mesa,votos_blancos_pres=votos_blancos_pres,votos_nulos_pres=votos_nulos_pres,
            votos_impugnados_pres=votos_imp_pres,votos_emitidos_pres=votos_tot_pres,votos_blancos_cons=votos_blancos_cons,
            votos_nulos_cons=votos_nulos_cons,votos_impugnados_cons=votos_imp_cons,votos_emitidos_cons=votos_tot_cons)
        acta.save()
        centro_votacion = self.mesa.centro_votacion
        distrito = centro_votacion.distrito
        provincia = distrito.provincia
        region = provincia.region
        for detalle in self.detalles:
            pres = "pres_"+str(detalle.partido.pk)
            votos_pres = self.request.POST[pres]
            cons = "cons_"+str(detalle.partido.pk)
            votos_cons = self.request.POST[cons]
            
            try:
                detalle_acta = DetalleActaRegional.objects.get(acta=acta,partido=detalle.partido)
            except DetalleActaRegional.DoesNotExist:
                detalle_acta = DetalleActaRegional(acta=acta,partido=detalle.partido)
                detalle_acta.votos_pres = 0
                detalle_acta.votos_cons = 0

            if not votos_pres.isnumeric():
                votos_pres=0
            else:
                try:
                    vot_pres = VotacionPresidenteRegional.objects.get(partido=detalle.partido, region=region)
                except VotacionPresidenteRegional.DoesNotExist:
                    vot_pres = VotacionPresidenteRegional(partido=detalle.partido, region=region)
                vot_pres.votos = vot_pres.votos + int(votos_pres) - detalle_acta.votos_pres
                vot_pres.save()
                
            if not votos_cons.isnumeric():
                votos_cons=0
            else:
                try:
                    vot_cons = VotacionConsejeroRegional.objects.get(partido=detalle.partido, provincia=provincia)
                except VotacionConsejeroRegional.DoesNotExist:
                    vot_cons = VotacionConsejeroRegional(partido=detalle.partido, provincia=provincia)
                vot_cons.votos = vot_cons.votos + int(votos_cons) - detalle_acta.votos_cons
                vot_cons.save()            
            
            detalle_acta.votos_pres=votos_pres
            detalle_acta.votos_cons=votos_cons
            detalle_acta.save()
        self.mesa.procesada_regional=True
        self.mesa.save()
        return HttpResponseRedirect(reverse('localizacion:mesa_regional')) 

def ProcesarActaMunicipal(FormView):
    template_name = "acta_municipal.html"
    form_class = FormularioActaMunicipal
    
    def get(self, request, *args, **kwargs):
        self.numero = kwargs['numero']
        return super(ProcesarActaMunicipal, self).get(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super(ProcesarActaMunicipal, self).get_initial()
        initial['mesa'] = self.numero
        initial['votos_blancos'] = 0
        initial['votos_nulos'] = 0
        initial['votos_impugnados'] = 0
        initial['votos_totales'] = 0
        return initial 
    
    def get_context_data(self, **kwargs):
        context = super(ProcesarActaMunicipal, self).get_context_data(**kwargs)
        mesa = Mesa.objects.get(numero=self.numero)
        centro_votacion = mesa.centro_votacion
        distrito = centro_votacion.distrito
        provincia = distrito.provincia
        region = provincia.region
        try:
            disenio_acta = DisenioActaMunicipal.objects.get(distrito=distrito)
            context['disenio_acta'] = disenio_acta
            detalles = DetalleDisenioActaMunicipal.objects.filter(disenio_acta=disenio_acta).order_by('id')       
            context['mesa'] = mesa
            context['detalles'] = detalles
            return context           
        except DisenioActaMunicipal.DoesNotExist:
            return HttpResponseRedirect(reverse('regional:mesa_presidencial'))
    
    def post(self, request, *args, **kwargs):
        mesa = Mesa.objects.get(numero=request.POST['mesa'])
        votos_blancos_prov = request.POST['voto_blanco_prov']
        votos_nulos_prov = request.POST['voto_nulo_prov']
        votos_imp_prov = request.POST['voto_impugnado_prov']
        votos_tot_prov = request.POST['voto_total_provincial']
        centro_votacion = mesa.centro_votacion
        distrito = centro_votacion.distrito
        provincia = distrito.provincia
        region = provincia.region
        if not distrito.capital_provincia:
            votos_blancos_dis = request.POST['voto_blanco_dis']
            votos_nulos_dis = request.POST['voto_nulo_dis']
            votos_imp_dis = request.POST['voto_impugnado_dis']
            votos_tot_dis = request.POST['voto_total_distrital']
        else:
            votos_blancos_dis = 0
            votos_nulos_dis = 0
            votos_imp_dis = 0
            votos_tot_dis = 0
        disenio_acta = DisenioActaMunicipal.objects.get(distrito=distrito)
        detalles = DetalleDisenioActaMunicipal.objects.filter(disenio_acta=disenio_acta).order_by('id') 
        acta = ActaMunicipal(mesa=mesa,votos_blancos_prov=votos_blancos_prov,votos_blancos_dis=votos_blancos_dis,
            votos_nulos_prov=votos_nulos_prov,votos_nulos_dis=votos_nulos_dis,
            votos_impugnados_prov=votos_imp_prov,votos_impugnados_dis=votos_imp_dis,
            votos_emitidos_prov=votos_tot_prov,votos_emitidos_dis=votos_tot_dis)
        acta.save()
        for detalle in detalles:
            prov = "prov_"+str(detalle.partido.pk)
            votos_provincial = request.POST[prov]
            dis = "dis_"+str(detalle.partido.pk)
            votos_distrital = request.POST[dis]
            
            try:
                detalle_acta = DetalleActaMunicipal.objects.get(acta=acta,partido=detalle.partido)
            except DetalleActaMunicipal.DoesNotExist:
                detalle_acta = DetalleActaMunicipal(acta=acta,partido=detalle.partido)
                detalle_acta.votos_provincial = 0
                detalle_acta.votos_distrital = 0

            if not votos_provincial.isnumeric():
                votos_provincial=0
            else:
                try:
                    vot_prov = VotacionProvincial.objects.get(partido=detalle.partido, provincia=provincia)
                except VotacionProvincial.DoesNotExist:
                    vot_prov = VotacionProvincial(partido=detalle.partido, provincia=provincia)
                vot_prov.votos = vot_prov.votos + int(votos_provincial) - detalle_acta.votos_provincial
                vot_prov.save()
                
            if not votos_distrital.isnumeric():
                votos_distrital=0
            else:
                try:
                    vot_dis = VotacionDistrital.objects.get(partido=detalle.partido, distrito=distrito)
                except VotacionDistrital.DoesNotExist:
                    vot_dis = VotacionDistrital(partido=detalle.partido, distrito=distrito)
                vot_dis.votos = vot_dis.votos + int(votos_distrital) - detalle_acta.votos_distrital
                vot_dis.save()
            
            
            detalle_acta.votos_provincial=votos_provincial
            detalle_acta.votos_distrital=votos_distrital
            detalle_acta.save()
        mesa.procesada_municipal=True
        mesa.save()
        return HttpResponseRedirect(reverse('localizacion:mesa_municipal'))

class BusquedaMesas(TemplateView):

    def get(self, request, *args, **kwargs):
        distrito = request.GET['distrito']
        centro_votacion = CentroVotacion.objects.filter(distrito=distrito)
        mesas = Mesa.objects.filter(centro_votacion=centro_votacion,procesada=False)
        if mesas:
            data = serializers.serialize('json', mesas, fields= ('numero'))
        else:
            data = []
        return HttpResponse(data, content_type='application/json')

def actas_municipales(request):
    actas = ActaMunicipal.objects.all()
    paginador = Paginator(actas, 10) 
    pagina = request.GET.get('pagina')
    try:
        actas = paginador.page(pagina)
    except PageNotAnInteger:      
        actas = paginador.page(1)
    except EmptyPage:      
        actas = paginador.page(paginador.num_pages)       
    context = {'localizacion':actas}
    return render(request, 'actas_municipales.html', context)

def actas_regionales(request):
    actas = ActaRegional.objects.all()
    paginador = Paginator(actas, 10) 
    pagina = request.GET.get('pagina')
    try:
        actas = paginador.page(pagina)
    except PageNotAnInteger:      
        actas = paginador.page(1)
    except EmptyPage:      
        actas = paginador.page(paginador.num_pages)       
    context = {'localizacion':actas}
    return render(request, 'actas_regionales.html', context)

def mesas(request):
    mesas = Mesa.objects.all().order_by('centro_votacion','numero')
    paginador = Paginator(mesas, 10) 
    pagina = request.GET.get('pagina')
    try:
        mesas = paginador.page(pagina)
    except PageNotAnInteger:      
        mesas = paginador.page(1)
    except EmptyPage:      
        mesas = paginador.page(paginador.num_pages)       
    context = {'mesas':mesas}
    return render(request, 'mesas.html', context)

def detalle_acta_municipal(request,acta):
    obj_acta = ActaMunicipal.objects.get(pk=acta)
    detalles = DetalleActaMunicipal.objects.filter(acta=acta)
    context = {'acta':obj_acta, 'detalles':detalles}
    return render(request, 'detalle_acta_municipal.html', context)

def detalle_acta_regional(request,acta):
    obj_acta = ActaRegional.objects.get(pk=acta)
    detalles = DetalleActaRegional.objects.filter(acta=acta)
    context = {'acta':obj_acta, 'detalles':detalles}
    return render(request, 'detalle_acta_regional.html', context)

def exportar_actas_municipales(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="actas_municipales.csv"'

    writer = csv.writer(response)
    writer.writerow(['MESA', 'VOTOS REGIONALES', 'VOTOS PROVINCIALES', 'VOTOS DISTRITALES'])
    actas = ActaMunicipal.objects.all()
    for acta in actas:
        writer.writerow([ActaMunicipal.mesa, ActaMunicipal.votos_emitidos_prov,ActaMunicipal.votos_emitidos_prov, ActaMunicipal.votos_emitidos_dis])
    return response

def exportar_mesas(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mesas.csv"'

    writer = csv.writer(response)
    writer.writerow(['MESA', 'CENTRO VOTACION', 'DISTRITO', 'NRO ELECTORES', 'PROCESAMIENTO'])
    mesas = Mesa.objects.all()
    for mesa in mesas:
        if mesa.procesada_municipal:
            procesada = "MESA PROCESADA MUNICIPAL"
        else:
            procesada = "MESA SIN PROCESAR"
        writer.writerow([mesa.numero, mesa.centro_votacion,mesa.centro_votacion.distrito, mesa.total_electores,procesada])
    return response

def reporte_presidente_regional(request, region):
    total_vb = ActaRegional.objects.filter(mesa=Mesa.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=Distrito.objects.filter(provincia=Provincia.objects.filter(region=region))))).aggregate(Sum('votos_blancos_pres'))
    total_vn = ActaRegional.objects.filter(mesa=Mesa.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=Distrito.objects.filter(provincia=Provincia.objects.filter(region=region))))).aggregate(Sum('votos_nulos_pres'))
    total_vi = ActaRegional.objects.filter(mesa=Mesa.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=Distrito.objects.filter(provincia=Provincia.objects.filter(region=region))))).aggregate(Sum('votos_impugnados_pres'))
    total_vv = VotacionConsejeroRegional.objects.filter(provincia=Provincia.objects.filter(region=region)).aggregate(Sum('votos'))
    total_votos = total_vv['votos__sum']+total_vb['votos_blancos_pres__sum']+total_vn['votos_nulos_pres__sum']+total_vi['votos_impugnados_pres__sum']
    votos_partidos = VotacionPresidenteRegional.objects.filter(region=region).order_by('-votos')
    context = {'votos_partidos':votos_partidos, 'region':region,'total_votos':total_votos,'total_vb':total_vb,'total_vn':total_vn,'total_vi':total_vi}
    return render(request, 'reporte_presidente_regional.html', context)

def reporte_consejero_regional(request, provincia):
    total_vb = ActaRegional.objects.filter(mesa=Mesa.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=Distrito.objects.filter(provincia=provincia)))).aggregate(Sum('votos_blancos_cons'))
    total_vn = ActaRegional.objects.filter(mesa=Mesa.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=Distrito.objects.filter(provincia=provincia)))).aggregate(Sum('votos_nulos_cons'))
    total_vi = ActaRegional.objects.filter(mesa=Mesa.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=Distrito.objects.filter(provincia=provincia)))).aggregate(Sum('votos_impugnados_cons'))
    total_vv = VotacionConsejeroRegional.objects.filter(provincia=provincia).aggregate(Sum('votos'))
    total_votos = total_vv['votos__sum']+total_vb['votos_blancos_cons__sum']+total_vn['votos_nulos_cons__sum']+total_vi['votos_impugnados_cons__sum']
    votos_partidos = VotacionConsejeroRegional.objects.filter(provincia=provincia).order_by('-votos')

    context = {'votos_partidos':votos_partidos, 'provincia':provincia,'total_votos':total_votos,'total_vb':total_vb,'total_vn':total_vn,'total_vi':total_vi}
    return render(request, 'reporte_consejero_regional.html', context)

def reporte_provincial(request, provincia):
    total_vb = ActaMunicipal.objects.filter(mesa=Mesa.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=Distrito.objects.filter(provincia=provincia)))).aggregate(Sum('votos_blancos_prov'))
    total_vn = ActaMunicipal.objects.filter(mesa=Mesa.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=Distrito.objects.filter(provincia=provincia)))).aggregate(Sum('votos_nulos_prov'))
    total_vi = ActaMunicipal.objects.filter(mesa=Mesa.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=Distrito.objects.filter(provincia=provincia)))).aggregate(Sum('votos_impugnados_prov'))
    total_vv = VotacionProvincial.objects.filter(provincia=provincia).aggregate(Sum('votos'))
    total_votos = total_vv['votos__sum']+total_vb['votos_blancos_prov__sum']+total_vn['votos_nulos_prov__sum']+total_vi['votos_impugnados_prov__sum']
    votos_partidos = VotacionProvincial.objects.filter(provincia=provincia).order_by('-votos')
    context = {'votos_partidos':votos_partidos,'provincia':provincia,'total_votos':total_votos,'total_vb':total_vb,'total_vn':total_vn,'total_vi':total_vi}
    return render(request, 'reporte_provincial.html', context)

def reporte_distrital(request, distrito):
    distrito_obj = Distrito.objects.get(pk=distrito)
    total_vb = ActaMunicipal.objects.filter(mesa=Mesa.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=distrito))).aggregate(Sum('votos_blancos_dis'))
    total_vn = ActaMunicipal.objects.filter(mesa=Mesa.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=distrito))).aggregate(Sum('votos_nulos_dis'))
    total_vi = ActaMunicipal.objects.filter(mesa=Mesa.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=distrito))).aggregate(Sum('votos_impugnados_dis'))
    total_vv = VotacionDistrital.objects.filter(distrito=distrito_obj).aggregate(Sum('votos'))
    total_votos = total_vv['votos__sum']+total_vb['votos_blancos_dis__sum']+total_vn['votos_nulos_dis__sum']+total_vi['votos_impugnados_dis__sum']
    votos_partidos = VotacionDistrital.objects.filter(distrito=distrito_obj).order_by('-votos')
    context = {'votos_partidos':votos_partidos,'distrito':distrito,'total_votos':total_votos,'total_vb':total_vb,'total_vn':total_vn,'total_vi':total_vi}
    return render(request, 'reporte_distrital.html', context)
            
def exportar_reporte_regional(request, region):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte-regional.csv"'

    writer = csv.writer(response)
    writer.writerow(['PARTIDO', 'REGION', 'VOTACION'])
    votos_partidos = VotacionPresidenteRegional.objects.filter(region=region).order_by('-votos')
    for votos_partido in votos_partidos:
        writer.writerow([votos_partido.partido, votos_partido.region, votos_partido.votos])
    return response

def exportar_reporte_provincial(request, provincia):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte-provincial.csv"'

    writer = csv.writer(response)
    writer.writerow(['PARTIDO', 'PROVINCIA', 'VOTACION'])
    votos_partidos = VotacionProvincial.objects.filter(provincia=provincia).order_by('-votos')
    for votos_partido in votos_partidos:
        writer.writerow([votos_partido.partido, votos_partido.provincia, votos_partido.votos])
    return response

def exportar_reporte_distrital(request, distrito):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte-distrital.csv"'

    writer = csv.writer(response)
    writer.writerow(['PARTIDO', 'DISTRITO', 'VOTACION'])
    votos_partidos = VotacionDistrital.objects.filter(distrito=distrito).order_by('-votos')
    for votos_partido in votos_partidos:
        writer.writerow([votos_partido.partido, votos_partido.distrito, votos_partido.votos])
    return response