from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from nacional.forms import FormularioMesaNacional, FormularioActaPresidencial,\
    FormularioActaCongresal
from nacional.models import MesaNacional, DisenioActaPresidencial,\
    DetalleDisenioActaPresidencial, ActaPresidencial, DetalleActaPresidencial,\
    VotacionPresidente, DisenioActaCongresal, DetalleDisenioActaCongresal,\
    ActaCongresal, DetalleActaCongresal, VotacionCongresalCandidato
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from localizacion.models import CentroVotacion, Provincia, Distrito, Partido
from django.db.models import Sum
from django.views.generic.list import ListView

# Create your views here.
class Tablero(TemplateView):
    template_name = "tablero_nacional.html"        

class MesaPresidencial(FormView):
    template_name = "mesa_presidencial.html"
    form_class = FormularioMesaNacional
    
    def get_context_data(self, **kwargs):
        mesas = MesaNacional.objects.filter(procesada_presidencial=False)
        context = super(MesaPresidencial, self).get_context_data(**kwargs)
        context['mesas'] = mesas
        return context
    
    def form_valid(self, form):
        data = form.cleaned_data
        mesa = data['mesas']
        try: 
            obj_mesa = MesaNacional.objects.get(pk=mesa)
            return HttpResponseRedirect(reverse('nacional:acta_presidencial', args=[mesa]))
        except MesaNacional.DoesNotExist:
            return HttpResponseRedirect(reverse('nacional:mesa_presidencial'))
        
class ProcesarActaPresidencial(FormView):
    template_name = "acta_presidencial.html"
    form_class = FormularioActaPresidencial
    
    def get(self, request, *args, **kwargs):
        self.numero = kwargs['numero']
        return super(ProcesarActaPresidencial, self).get(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super(ProcesarActaPresidencial, self).get_initial()
        initial['mesa'] = self.numero
        initial['votos_blancos'] = 0
        initial['votos_nulos'] = 0
        initial['votos_impugnados'] = 0
        initial['votos_totales'] = 0
        return initial 
    
    def get_context_data(self, **kwargs):
        context = super(ProcesarActaPresidencial, self).get_context_data(**kwargs)
        mesa = MesaNacional.objects.get(numero=self.numero)
        try:
            disenio_acta = DisenioActaPresidencial.objects.get(pk=1) 
            context['disenio_acta'] = disenio_acta
            detalles = DetalleDisenioActaPresidencial.objects.filter(disenio_acta=disenio_acta).order_by('id')        
            context['mesa'] = mesa
            context['detalles'] = detalles
            return context           
        except DisenioActaPresidencial.DoesNotExist:
            return HttpResponseRedirect(reverse('nacional:mesa_presidencial'))            
    
    def post(self, request, *args, **kwargs):
        mesa = MesaNacional.objects.get(numero=request.POST['mesa'])
        votos_blancos = request.POST['votos_blancos']
        votos_nulos = request.POST['votos_nulos']
        votos_imp = request.POST['votos_impugnados']
        votos_tot = request.POST['votos_totales']
        acta = ActaPresidencial(mesa=mesa,votos_blancos=votos_blancos,votos_nulos=votos_nulos,votos_impugnados=votos_imp,votos_emitidos=votos_tot)
        acta.save()
        centro_votacion = mesa.centro_votacion
        distrito = centro_votacion.distrito
        provincia = distrito.provincia
        region = provincia.region
        disenio_acta = DisenioActaPresidencial.objects.get(pk=1)
        detalles = DetalleDisenioActaPresidencial.objects.filter(disenio_acta=disenio_acta).order_by('id')
        for detalle in detalles:
            pres = "pres_"+str(detalle.partido.pk)
            votos_pres = self.request.POST[pres]
            print votos_pres
            try:
                detalle_acta = DetalleActaPresidencial.objects.get(acta=acta,partido=detalle.partido)
            except DetalleActaPresidencial.DoesNotExist:
                detalle_acta = DetalleActaPresidencial(acta=acta,partido=detalle.partido)              
                detalle_acta.votos = 0
            if not votos_pres.isnumeric():
                votos_pres=0
            else:
                try:
                    vot_pres = VotacionPresidente.objects.get(partido=detalle.partido)
                except VotacionPresidente.DoesNotExist:
                    vot_pres = VotacionPresidente(partido=detalle.partido)
                vot_pres.votos = vot_pres.votos + int(votos_pres) - detalle_acta.votos
                vot_pres.save()                
            detalle_acta.votos=votos_pres
            detalle_acta.save()
        mesa.procesada_presidencial=True
        mesa.save()
        return HttpResponseRedirect(reverse('nacional:mesa_presidencial'))
    
class MesaCongresal(FormView):
    template_name = "mesa_congresal.html"
    form_class = FormularioMesaNacional
    
    def get_context_data(self, **kwargs):
        mesas = MesaNacional.objects.filter(procesada_congresal=False)
        context = super(MesaCongresal, self).get_context_data(**kwargs)
        context['mesas'] = mesas
        return context
    
    def form_valid(self, form):
        data = form.cleaned_data
        mesa = data['mesas']
        try: 
            obj_mesa = MesaNacional.objects.get(pk=mesa)
            return HttpResponseRedirect(reverse('nacional:acta_congresal', args=[mesa]))
        except MesaNacional.DoesNotExist:
            return HttpResponseRedirect(reverse('nacional:mesa_congresal'))
        
class ProcesarActaCongresal(FormView):
    template_name = "acta_congresal.html"
    form_class = FormularioActaCongresal
    
    def get(self, request, *args, **kwargs):
        self.numero = kwargs['numero']
        return super(ProcesarActaCongresal, self).get(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super(ProcesarActaCongresal, self).get_initial()
        initial['mesa'] = self.numero
        initial['votos_blancos'] = 0
        initial['votos_nulos'] = 0
        initial['votos_impugnados'] = 0
        initial['votos_totales'] = 0
        return initial 
    
    def get_context_data(self, **kwargs):
        context = super(ProcesarActaCongresal, self).get_context_data(**kwargs)
        mesa = MesaNacional.objects.get(numero=self.numero)
        try:
            disenio_acta = DisenioActaCongresal.objects.get(region=mesa.centro_votacion.distrito.provincia.region) 
            context['disenio_acta'] = disenio_acta
            detalles = DetalleDisenioActaCongresal.objects.filter(disenio_acta=disenio_acta).order_by('id')        
            context['mesa'] = mesa
            context['detalles'] = detalles
            return context           
        except DisenioActaCongresal.DoesNotExist:
            return HttpResponseRedirect(reverse('nacional:mesa_congresal'))            
    
    def post(self, request, *args, **kwargs):
        mesa = MesaNacional.objects.get(numero=request.POST['mesa'])
        votos_blancos = request.POST['votos_blancos']
        votos_nulos = request.POST['votos_nulos']
        votos_imp = request.POST['votos_impugnados']
        votos_tot = request.POST['votos_totales']
        acta = ActaCongresal(mesa=mesa,votos_blancos=votos_blancos,votos_nulos=votos_nulos,votos_impugnados=votos_imp,votos_emitidos=votos_tot)
        acta.save()
        centro_votacion = mesa.centro_votacion
        distrito = centro_votacion.distrito
        provincia = distrito.provincia
        region = provincia.region
        disenio_acta = DisenioActaCongresal.objects.get(region=mesa.centro_votacion.distrito.provincia.region)
        detalles = DetalleDisenioActaCongresal.objects.filter(disenio_acta=disenio_acta).order_by('id')
        for detalle in detalles:
            cong_total = "total_"+str(detalle.partido.pk)
            votos_cong_total = self.request.POST[cong_total]
            if not votos_cong_total.isnumeric():
                votos_cong_total=0
            else:
                try:
                    vot_cong_tot = VotacionCongresalCandidato.objects.get(partido=detalle.partido,region=region)
                except VotacionCongresalCandidato.DoesNotExist:
                    vot_cong_tot = VotacionCongresalCandidato(partido=detalle.partido,region=region)
                vot_cong_tot.votos += int(votos_cong_total)
                vot_cong_tot.save()
            for i in range(1,8):
                cong = "cong_"+str(detalle.partido.pk)+"_"+str(i)
                votos_cong = self.request.POST[cong]
                try:
                    detalle_acta = DetalleActaCongresal.objects.get(acta=acta,partido=detalle.partido,numero=i)
                except DetalleActaCongresal.DoesNotExist:
                    detalle_acta = DetalleActaCongresal(acta=acta,partido=detalle.partido,numero=i)              
                    detalle_acta.votos = 0
                if not votos_cong.isnumeric():
                    votos_cong=0
                else:
                    try:
                        vot_cong = VotacionCongresalCandidato.objects.get(partido=detalle.partido,region=region,numero=i)
                    except VotacionCongresalCandidato.DoesNotExist:
                        vot_cong = VotacionCongresalCandidato(partido=detalle.partido,region=region,numero=i)
                    vot_cong.votos = vot_cong.votos + int(votos_cong) - detalle_acta.votos
                    vot_cong.save()                
                detalle_acta.votos = votos_cong
                detalle_acta.save()
        mesa.procesada_congresal=True
        mesa.save()
        return HttpResponseRedirect(reverse('nacional:mesa_congresal'))
    
class ReportePresidente(TemplateView):
    template_name = "reporte_presidente.html"
    
    def get_context_data(self, **kwargs):
        context = super(ReportePresidente, self).get_context_data(**kwargs)
        total_vb = ActaPresidencial.objects.filter(mesa=MesaNacional.objects.filter(centro_votacion=CentroVotacion.objects.all())).aggregate(Sum('votos_blancos'))            
        if total_vb['votos_blancos__sum'] is None:
            total_vb['votos_blancos__sum'] = 0        
        total_vn = ActaPresidencial.objects.filter(mesa=MesaNacional.objects.filter(centro_votacion=CentroVotacion.objects.all())).aggregate(Sum('votos_nulos'))
        if total_vn['votos_nulos__sum'] is None:
            total_vn['votos_nulos__sum'] = 0
        total_vi = ActaPresidencial.objects.filter(mesa=MesaNacional.objects.filter(centro_votacion=CentroVotacion.objects.all())).aggregate(Sum('votos_impugnados'))
        if total_vi['votos_impugnados__sum'] is None:
            total_vi['votos_impugnados__sum'] = 0
        total_vv = VotacionPresidente.objects.all().aggregate(Sum('votos'))
        if total_vv['votos__sum'] is None:
            total_vv['votos__sum'] = 0
        total_votos = total_vv['votos__sum']+total_vb['votos_blancos__sum']+total_vn['votos_nulos__sum']+total_vi['votos_impugnados__sum']
        votos_partidos = VotacionPresidente.objects.all().order_by('-votos')
        context['total_vb'] = total_vb
        context['total_vn'] = total_vn
        context['total_vi'] = total_vi
        context['total_votos'] = total_votos
        context['votos_partidos'] = votos_partidos
        return context
    
class ActasPresidenciales(ListView):
    model = ActaPresidencial
    template_name = 'actas_presidenciales.html'
    context_object_name = 'actas'
    queryset = ActaPresidencial.objects.all()
    
class ActasCongresales(ListView):
    model = ActaCongresal
    template_name = 'actas_congresales.html'
    context_object_name = 'actas'
    queryset = ActaCongresal.objects.all()
    
class MesasNacionales(ListView):
    model = MesaNacional
    template_name = 'mesas_nacionales.html'
    context_object_name = 'mesas'
    queryset = MesaNacional.objects.all()
    
class ReporteCongresal(TemplateView):
    template_name = "reporte_congresal.html"
    
    def get(self, request, *args, **kwargs):
        self.region = kwargs['region']
        return super(ReporteCongresal, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ReporteCongresal, self).get_context_data(**kwargs)
        total_vb = ActaCongresal.objects.filter(mesa=MesaNacional.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=Distrito.objects.filter(provincia=Provincia.objects.filter(region=self.region))))).aggregate(Sum('votos_blancos'))            
        if total_vb['votos_blancos__sum'] is None:
            total_vb['votos_blancos__sum'] = 0        
        total_vn = ActaCongresal.objects.filter(mesa=MesaNacional.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=Distrito.objects.filter(provincia=Provincia.objects.filter(region=self.region))))).aggregate(Sum('votos_nulos'))
        if total_vn['votos_nulos__sum'] is None:
            total_vn['votos_nulos__sum'] = 0
        total_vi = ActaCongresal.objects.filter(mesa=MesaNacional.objects.filter(centro_votacion=CentroVotacion.objects.filter(distrito=Distrito.objects.filter(provincia=Provincia.objects.filter(region=self.region))))).aggregate(Sum('votos_impugnados'))
        if total_vi['votos_impugnados__sum'] is None:
            total_vi['votos_impugnados__sum'] = 0
        total_vv = VotacionCongresalCandidato.objects.all().aggregate(Sum('votos'))
        if total_vv['votos__sum'] is None:
            total_vv['votos__sum'] = 0
        total_votos = total_vv['votos__sum']+total_vb['votos_blancos__sum']+total_vn['votos_nulos__sum']+total_vi['votos_impugnados__sum']
        resultados = {}
        partidos = Partido.objects.all().order_by('nombre')
        for partido in partidos:
            congresistas = []
            votos_partidos = VotacionCongresalCandidato.objects.filter(partido=partido).order_by('numero')
            for voto in votos_partidos:
                congresistas.append(voto.votos)
            resultados[partido.nombre]=congresistas
        context['total_vb'] = total_vb
        context['total_vn'] = total_vn
        context['total_vi'] = total_vi
        context['total_votos'] = total_votos
        context['resultados'] = resultados
        return context