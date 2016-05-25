from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_str

class Vista(models.Model):
    nombre = models.CharField(max_length=150)

    class Meta:
        unique_together = (('nombre'),)

    def __str__(self):
        return self.nombre    

class Perfil(models.Model):
    nombre = models.CharField(max_length=150)

    class Meta:
        unique_together = (('nombre'),)

    def __str__(self):
        return self.nombre

class PermisoPerfil(models.Model):
    perfil = models.ForeignKey(Perfil)
    vista = models.ForeignKey(Vista)

    class Meta:
        unique_together = (('perfil', 'vista'),)

class UsuarioPerfil(models.Model):
    usuario = models.ForeignKey(User)
    perfil = models.ForeignKey(Perfil)

    class Meta:
        unique_together = (('usuario', 'perfil'),)
        
class Opcion(models.Model):
    nombre = models.CharField(max_length=150)
    modulo = models.CharField(max_length=100)
    vistas = models.ManyToManyField(Vista)
    
    def __str__(self):
        return smart_str(self.nombre)
    
    class Meta:
        unique_together = (('nombre'),)
    
class OpcionPerfil(models.Model):
    opcion = models.ForeignKey(Opcion)
    perfil = models.ForeignKey(Perfil)