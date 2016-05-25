from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from seguridad.views import Inicio, Login, CambiarPassword, CrearPermiso, CrearVista, ReportePermisos, ReporteVistas, BorrarPermiso, CrearPerfil, ReportePerfiles, CrearPermisoPerfil,ReportePermisosPerfil,CrearPerfilUsuario, BorrarPermisoPerfil, Permisos, PermisoDenegado,\
    ReporteUsuariosPerfil, ReporteUsuarios, ReportePerfilesUsuario, CrearOpcion,\
    AplicacionesProyecto, CrearPermisoOpcion, ReporteOpcionesPerfil,\
    ReporteVistasOpcion, OpcionesAplicacion, ReporteAplicacionesPerfil
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', Login.as_view(), name="login"),
    url(r'^inicio/$',login_required(Inicio.as_view()), name="inicio"),
    url(r'^permisos/$',login_required(Permisos.as_view()), name="permisos"),
    url(r'^permiso_denegado/$', login_required(PermisoDenegado.as_view()), name="permiso_denegado"),
    url(r'^cambiar_password$', login_required(CambiarPassword.as_view()), name="cambiar_password"),
    url(r'^crear_permiso$', login_required(CrearPermiso.as_view()), name="crear_permiso"),
    url(r'^reporte_permisos$', login_required(ReportePermisos.as_view()), name="reporte_permisos"),
    url(r'^reporte_vistas$', login_required(ReporteVistas.as_view()), name="reporte_vistas"),
    url(r'^reporte_perfiles$', login_required(ReportePerfiles.as_view()), name="reporte_perfiles"),
    url(r'^crear_vista$', login_required(CrearVista.as_view()), name="crear_vista"),
    url(r'^crear_perfil$', login_required(CrearPerfil.as_view()), name="crear_perfil"),
    url(r'^aplicaciones_proyecto', login_required(AplicacionesProyecto.as_view()), name="aplicaciones_proyecto"),
    url(r'^crear_opcion/(?P<aplicacion>.+)/$', login_required(CrearOpcion.as_view()), name="crear_opcion"),
    url(r'^opciones_aplicacion/(?P<aplicacion>.+)/(?P<perfil>.+)/$', login_required(OpcionesAplicacion.as_view()), name="opciones_aplicacion"),
    url(r'^salir$', logout, name="salir", kwargs={'next_page': '/'}),
    url(r'^borrar_permiso/(?P<pk>\d+)/$',BorrarPermiso.as_view(), name="borrar_permiso"),
    url(r'^borrar_permiso_perfil/(?P<pk>\d+)/$',BorrarPermisoPerfil.as_view(), name="borrar_permiso_perfil"),
    url(r'^crear_permiso_perfil$', login_required(CrearPermisoPerfil.as_view()), name="crear_permiso_perfil"),
    url(r'^reporte_aplicaciones_perfil/(?P<perfil>\d+)/$', login_required(ReporteAplicacionesPerfil.as_view()), name="reporte_aplicaciones_perfil"),
    url(r'^reporte_opciones_perfil/(?P<perfil>\d+)/(?P<aplicacion>.+)/$', login_required(ReporteOpcionesPerfil.as_view()), name="reporte_opciones_perfil"),
    url(r'^reporte_permisos_perfil/(?P<perfil>\d+)/$', login_required(ReportePermisosPerfil.as_view()), name="reporte_permisos_perfil"),        
    url(r'^crear_perfil_usuario$', login_required(CrearPerfilUsuario.as_view()), name="crear_perfil_usuario"),
    url(r'^reporte_usuarios/$', login_required(ReporteUsuarios.as_view()), name="reporte_usuarios"),  
    url(r'^reporte_usuarios_perfil/(?P<perfil>\d+)/$', login_required(ReporteUsuariosPerfil.as_view()), name="reporte_usuarios_perfil"),
    url(r'^reporte_vistas_opcion/(?P<opcion>\d+)/$', login_required(ReporteVistasOpcion.as_view()), name="reporte_vistas_opcion"),
    url(r'^reporte_perfiles_usuario/(?P<usuario>\d+)/$', login_required(ReportePerfilesUsuario.as_view()), name="reporte_perfiles_usuario"),
    url(r'^crear_permiso_opcion/$', login_required(CrearPermisoOpcion.as_view()), name="crear_permiso_opcion"),        
)