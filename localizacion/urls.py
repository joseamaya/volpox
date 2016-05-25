from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from localizacion.views import Tablero, BusquedaProvincias, BusquedaDistritos,\
    seleccion_distrito, seleccion_prov_consejero, seleccion_provincia,\
    seleccion_region

urlpatterns = patterns('',
    url(r'^tablero/$',login_required(Tablero.as_view()), name="tablero"),
    url(r'^busquedaProvincias/$',login_required(BusquedaProvincias.as_view()), name="busquedaProvincias"),
    url(r'^busquedaDistritos/$',login_required(BusquedaDistritos.as_view()), name="busquedaDistritos"),
    url(r'^seleccion_distrito/$',login_required(seleccion_distrito), name="seleccion_distrito"),
    url(r'^seleccion_prov_consejero/$',login_required(seleccion_prov_consejero), name="seleccion_prov_consejero"),
    url(r'^seleccion_provincia/$',login_required(seleccion_provincia), name="seleccion_provincia"),
    url(r'^seleccion_region/$',login_required(seleccion_region), name="seleccion_region"),
)