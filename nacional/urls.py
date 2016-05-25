from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from nacional.views import MesaPresidencial, Tablero, ProcesarActaPresidencial,\
    ReportePresidente, ActasPresidenciales, MesasNacionales, MesaCongresal,\
    ProcesarActaCongresal, ActasCongresales, ReporteCongresal

urlpatterns = patterns('',
    url(r'^tablero/$',login_required(Tablero.as_view()), name="tablero"),
    url(r'^mesa_presidencial/$',login_required(MesaPresidencial.as_view()), name="mesa_presidencial"),
    url(r'^mesa_congresal/$',login_required(MesaCongresal.as_view()), name="mesa_congresal"),
    url(r'^reporte_presidente/$',login_required(ReportePresidente.as_view()), name="reporte_presidente"),
    url(r'^acta_presidencial/(?P<numero>\d+)/$',login_required(ProcesarActaPresidencial.as_view()), name="acta_presidencial"),
    url(r'^acta_congresal/(?P<numero>\d+)/$',login_required(ProcesarActaCongresal.as_view()), name="acta_congresal"),
    url(r'^actas_presidenciales/$',login_required(ActasPresidenciales.as_view()), name="actas_presidenciales"),
    url(r'^actas_congresales/$',login_required(ActasCongresales.as_view()), name="actas_congresales"),
    url(r'^mesas_nacionales/$',login_required(MesasNacionales.as_view()), name="mesas_nacionales"),
    url(r'^reporte_congresal/(?P<region>\d+)/$',login_required(ReporteCongresal.as_view()), name="reporte_congresal"),    
)