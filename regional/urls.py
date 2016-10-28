from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from regional.views import ProcesarMesaMunicipal, ProcesarMesaRegional,\
    BusquedaMesas, ProcesarActaRegional, actas_municipales,\
    actas_regionales, mesas, detalle_acta_municipal, detalle_acta_regional,\
    exportar_actas_municipales, exportar_mesas, exportar_reporte_regional,\
    exportar_reporte_provincial, exportar_reporte_distrital,\
    reporte_presidente_regional, reporte_consejero_regional, reporte_provincial,\
    reporte_distrital, Tablero

urlpatterns = [
    url(r'^tablero/$',login_required(Tablero.as_view()), name="tablero"),
    url(r'^mesa_municipal/$',login_required(ProcesarMesaMunicipal.as_view()), name="mesa_municipal"),
    url(r'^mesa_regional/$',login_required(ProcesarMesaRegional.as_view()), name="mesa_regional"),
    url(r'^busquedaMesas/$',login_required(BusquedaMesas.as_view()), name="busquedaMesas"),
    #url(r'^acta_municipal/(?P<numero>\d+)/$',login_required(acta_municipal), name="acta_municipal"),
    url(r'^acta_regional/(?P<numero>\d+)/$',login_required(ProcesarActaRegional.as_view()), name="acta_regional"),
    url(r'^actas_municipales/$',login_required(actas_municipales), name="actas_municipales"),
    url(r'^actas_regionales/$',login_required(actas_regionales), name="actas_regionales"),
    url(r'^mesas/$',login_required(mesas), name="mesas"),
    url(r'^detalle_acta_municipal/(?P<acta>\d+)/$',login_required(detalle_acta_municipal), name="detalle_acta_municipal"),
    url(r'^detalle_acta_regional/(?P<acta>\d+)/$',login_required(detalle_acta_regional), name="detalle_acta_regional"),    
    url(r'^exportar_actas_municipales/$',login_required(exportar_actas_municipales), name="exportar_actas_municipales"),
    url(r'^exportar_mesas/$',login_required(exportar_mesas), name="exportar_mesas"),
    url(r'^exportar_reporte_regional/(?P<region>\d+)/$',login_required(exportar_reporte_regional), name="exportar_reporte_regional"),
    url(r'^exportar_reporte_provincial/(?P<provincia>\d+)/$',login_required(exportar_reporte_provincial), name="exportar_reporte_provincial"),
    url(r'^exportar_reporte_distrital/(?P<distrito>\d+)/$',login_required(exportar_reporte_distrital), name="exportar_reporte_distrital"),
    url(r'^reporte_presidente_regional/(?P<region>\d+)/$',login_required(reporte_presidente_regional), name="reporte_presidente_regional"),
    url(r'^reporte_consejero_regional/(?P<provincia>\d+)/$',login_required(reporte_consejero_regional), name="reporte_consejero_regional"),
    url(r'^reporte_provincial/(?P<provincia>\d+)/$',login_required(reporte_provincial), name="reporte_provincial"),
    url(r'^reporte_distrital/(?P<distrito>\d+)/$',login_required(reporte_distrital), name="reporte_distrital"),        
]