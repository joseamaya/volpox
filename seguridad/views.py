from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from seguridad.forms import FormularioCambioPassword,FormularioLogin,\
    FormularioPerfiles
from django.views.generic import View
from seguridad.models import Vista, Perfil, PermisoPerfil,UsuarioPerfil,\
    Opcion, OpcionPerfil
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.views import logout
from django.contrib.auth.models import User
import sys, inspect
import volpox.settings

class Permiso():
    
    def revisar_permisos(self, usuario):        
        nombre_clase = self.__class__.__name__
        try:
            perfiles=UsuarioPerfil.objects.filter(usuario=usuario)
            for perfil_usuario in perfiles:
                try:
                    vista=Vista.objects.get(nombre=nombre_clase)
                except Vista.DoesNotExist:
                    vista = Vista()
                    vista.nombre = nombre_clase
                    vista.save()
                opciones = vista.opcion_set.all()
                for opcion in opciones:
                    try:
                        OpcionPerfil.objects.get(opcion=opcion,perfil=perfil_usuario.perfil)
                        return True
                    except:
                        pass
            return False        
        except UsuarioPerfil.DoesNotExist:
            return False
        
    def obtener_opciones(self,usuario):
        perfiles=UsuarioPerfil.objects.filter(usuario=usuario)
        lista_opciones =[]
        for perfil_usuario in perfiles:
            permisos_opciones = OpcionPerfil.objects.filter(perfil=perfil_usuario.perfil)
            for permiso_opcion in permisos_opciones:
                lista_opciones.append(permiso_opcion.opcion.nombre)
        return lista_opciones

class Inicio(View):
    
    def get(self, request, *args, **kwargs):
        
        return render(request,'bienvenida.html')
    
class Login(View):
    
    def get(self, request, *args, **kwargs):
        form = FormularioLogin()
        context = {'form':form}
        return render(request, 'login.html',context)

    def post(self, request, *args, **kwargs):
        form = FormularioLogin(request.POST)
        if form.is_valid():
            r_username = request.POST['usuario']
            r_password = request.POST['password']
            usuario = authenticate(username=r_username, password=r_password)
            login(request, usuario)
            return HttpResponseRedirect(reverse('seguridad:inicio'))                         
        context = {'form':form}
        return render(request, 'login.html', context)       

class CambiarPassword(View):

    def get(self, request, *args, **kwargs):
        form = FormularioCambioPassword(request.user)
        context = {'form':form}
        return render(request, 'cambiar_password.html', context)

    def post(self, request, *args, **kwargs):
        usuario = request.user
        form = FormularioCambioPassword(usuario,request.POST)
        if form.is_valid():
            password_nueva=request.POST['password_nueva']
            usuario.set_password(password_nueva)
            usuario.save()
            logout(request)
            return HttpResponseRedirect(reverse('seguridad:login'))
        context = {'form':form}
        return render(request, 'cambiar_password.html', context)

class Permisos(Permiso, View):

    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))

    def get(self, request, *args, **kwargs):
        return render(request,'bienvenida_permisos.html')
    
class PermisoDenegado(View):
    def get(self, request, *args, **kwargs):
        return render(request,'permiso_denegado.html')

class CrearPermiso(CreateView):
    model = Permiso
    fields = ['usuario','vista']
    template_name = 'crear_permiso.html'
    success_url = reverse_lazy('seguridad:crear_permiso')

class CrearPermisoPerfil(Permiso, CreateView):
    model = PermisoPerfil
    fields = ['perfil','vista']
    template_name = 'crear_permiso_perfil.html'
    success_url = reverse_lazy('seguridad:crear_permiso_perfil')
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))

class CrearPerfilUsuario2(CreateView):
    model = UsuarioPerfil
    fields = ['usuario','perfil']
    template_name = 'crear_perfil_usuario.html'
    success_url = reverse_lazy('seguridad:crear_perfil_usuario')
    
class CrearPerfilUsuario(Permiso, View):  
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))
    
    def get(self, request, *args, **kwargs):
        try:
            usuarios = User.objects.all().order_by('username')            
            perfiles = Perfil.objects.all().order_by('nombre') 
            context={'usuarios':usuarios,'perfiles':perfiles}             
            return render(request, 'crear_perfil_usuario.html',context)
        except:
            return HttpResponseRedirect(reverse('reclamos:busqueda_simulacion_baja_deudas'))        
    
    def post(self, request, *args, **kwargs):
        expediente = request.POST['expediente']  
        return self.exportar_simulacion_deudas_prescritas(request,expediente)

class AplicacionesProyecto(Permiso, View):    
    
    def get(self, request, *args, **kwargs):
        aplicaciones = [ app for app in siad.settings.INSTALLED_APPS if not "django" in app ]
        context={'aplicaciones':aplicaciones}             
        return render(request, 'reporte_aplicaciones.html',context)
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))
    
class CrearOpcion(Permiso, View):
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))
    
    def get(self, request, *args, **kwargs):
        aplicacion = self.kwargs['aplicacion']
        lista_clases = []
        for nombre_modulo,instancia_modulo in inspect.getmembers(sys.modules[aplicacion]):
            if nombre_modulo=='views':
                codigo_fuente = inspect.getsource(instancia_modulo)
                codigo_fuente = codigo_fuente.replace(" ", "")
                for miembro in dir(instancia_modulo):
                    obj = getattr(instancia_modulo, miembro)
                    if inspect.isclass(obj):
                        cadena_clase = 'class' + miembro
                        if codigo_fuente.find(cadena_clase)>=0:
                            lista_clases.append(miembro)
        context={'vistas':lista_clases,'aplicacion':aplicacion}
        return render(request, 'reporte_vistas_aplicacion.html',context)
    
    def post(self, request, *args, **kwargs):
        nombre_vista = request.POST['nombre_vista']
        aplicacion = request.POST['aplicacion']
        vistas = request.POST.getlist('vistas')
        try:
            opcion = Opcion.objects.get(nombre=nombre_vista)
        except:
            opcion = Opcion()
            opcion.nombre = nombre_vista
            opcion.modulo= aplicacion
            opcion.save()
        for vista in vistas:
            try:
                vista_obj = Vista.objects.get(nombre=vista)
            except Vista.DoesNotExist:
                vista_obj = Vista()
                vista_obj.nombre = vista
                vista_obj.save()
            opcion.vistas.add(vista_obj)
        return HttpResponseRedirect(reverse('seguridad:aplicaciones_proyecto'))
        
class CrearPerfil(Permiso, CreateView):
    model = Perfil
    fields = ['nombre']
    template_name = 'crear_perfil.html'
    success_url = reverse_lazy('seguridad:crear_perfil')
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))

class CrearVista(Permiso, CreateView):
    model = Vista
    fields = ['nombre']
    template_name = 'crear_vista.html'
    success_url = reverse_lazy('seguridad:crear_vista')
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))

class BorrarPermiso(DeleteView):
    model = Permiso
    template_name = 'borrar_permiso.html'
    success_url = reverse_lazy('seguridad:reporte_permisos')

class BorrarPermisoPerfil(DeleteView):
    model = PermisoPerfil
    template_name = 'borrar_permiso_perfil.html'
    success_url = reverse_lazy('seguridad:reporte_permisos_perfil')

class ReportePermisos(ListView):
    model = Permiso
    template_name = 'reporte_permisos.html'
    context_object_name = 'permisos'
    paginate_by = 15

class ReporteVistas(Permiso, ListView):
    model = Vista
    template_name = 'reporte_vistas.html'
    context_object_name = 'vistas'
    paginate_by = 15
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))

class ReportePerfiles(Permiso, ListView):
    model = Perfil
    template_name = 'reporte_perfiles.html'
    context_object_name = 'perfiles'
    paginate_by = 15
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))

class ReporteUsuariosPerfil(Permiso, ListView):
    template_name = 'reporte_usuarios_perfil.html'
    context_object_name = 'usuarios'
    paginate_by = 15
    
    def get_queryset(self,*args,**kwargs):
        perfil = self.kwargs['perfil']
        return UsuarioPerfil.objects.filter(perfil=Perfil.objects.get(pk=perfil))
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))

class ReporteAplicacionesPerfil(Permiso, View):
    
    def get(self, request, *args, **kwargs):
        perfil = self.kwargs['perfil']
        aplicaciones = [ app for app in siad.settings.INSTALLED_APPS if not "django" in app ]
        context={'perfil':perfil,'aplicaciones':aplicaciones}
        return render(request, 'reporte_aplicaciones_perfil.html',context)
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))

class ReporteOpcionesPerfil(Permiso, ListView):
    template_name = 'reporte_opciones_perfil.html'
    context_object_name = 'opciones'
    paginate_by = 15
    
    def get_queryset(self,*args,**kwargs):
        perfil = self.kwargs['perfil']
        aplicacion = self.kwargs['aplicacion']
        opciones = Opcion.objects.filter(modulo=aplicacion)
        lista_opciones = []
        for opcion in opciones:
            if len(opcion.opcionperfil_set.filter(perfil=perfil))>0:
                lista_opciones.append(opcion)
        return lista_opciones
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))
        
class ReporteVistasOpcion(Permiso, ListView):
    template_name = 'reporte_vistas_opcion.html'
    context_object_name = 'vistas'
    paginate_by = 15
    
    def get_queryset(self,*args,**kwargs):
        opcion = Opcion.objects.get(pk=self.kwargs['opcion'])
        vistas = opcion.vistas.all()
        return vistas
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))

class ReportePerfilesUsuario(Permiso, ListView):
    template_name = 'reporte_perfiles_usuario.html'
    context_object_name = 'perfiles_usuario'
    paginate_by = 15
    
    def get_queryset(self,*args,**kwargs):
        usuario = self.kwargs['usuario']
        return UsuarioPerfil.objects.filter(usuario=usuario).order_by('perfil')
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))
    
class ReporteUsuarios(Permiso, ListView):
    model = User
    template_name = 'reporte_usuarios.html'
    context_object_name = 'usuarios'
    paginate_by = 15
    
    def get_queryset(self,*args,**kwargs):
        return User.objects.all().order_by('username')
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))
    
class ReportePermisosPerfil(Permiso, ListView):
    template_name = 'reporte_permisos_perfil.html'
    context_object_name = 'permisos'
    paginate_by = 15
    
    def get_queryset(self,*args,**kwargs):
        perfil = self.kwargs['perfil']
        return PermisoPerfil.objects.filter(perfil=Perfil.objects.get(pk=perfil)).order_by('vista__nombre')
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))
    
class CrearPermisoOpcion(Permiso, View):
    
    def dispatch(self, request, *args, **kwargs):
        if self.revisar_permisos(request.user):
            clase = type(self)
            return super(clase, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('seguridad:permiso_denegado'))
        
    def get(self, request, *args, **kwargs):
        form = FormularioPerfiles()
        context={'form':form}
        return render(request, 'crear_permiso_opcion.html',context)        

    def post(self, request, *args, **kwargs):
        perfil = request.POST['perfil']
        aplicacion = request.POST['aplicaciones']
        return HttpResponseRedirect(reverse('seguridad:opciones_aplicacion', args=[aplicacion,perfil]))
    
class OpcionesAplicacion(Permiso, ListView):
    
    def get(self, request, *args, **kwargs):
        perfil = Perfil.objects.get(pk=self.kwargs['perfil'])
        aplicacion = self.kwargs['aplicacion']
        opciones = Opcion.objects.filter(modulo=aplicacion)
        lista_opciones = []
        for opcion in opciones:
            if len(opcion.opcionperfil_set.filter(perfil=perfil))<=0:
                lista_opciones.append(opcion)
        context={'perfil':perfil,'opciones':lista_opciones}
        return render(request, 'opciones_aplicacion.html',context)
    
    def post(self, request, *args, **kwargs):
        perfil = request.POST['perfil']
        opciones = request.POST.getlist('opciones')
        for opcion in opciones:
            opcion_perfil = OpcionPerfil()
            opcion_perfil.perfil = Perfil.objects.get(nombre=perfil)
            opcion_perfil.opcion = Opcion.objects.get(pk=opcion)
            opcion_perfil.save()            
        return HttpResponseRedirect(reverse('seguridad:crear_permiso_opcion'))