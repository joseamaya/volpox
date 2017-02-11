from django.db import models
from localizacion.models import CentroVotacion, Partido, Region, Provincia, Distrito

# Create your models here.
class Mesa(models.Model):
    numero = models.CharField(max_length=6, primary_key=True)
    total_electores = models.IntegerField()
    centro_votacion = models.ForeignKey(CentroVotacion)
    procesada_municipal = models.BooleanField(default=False)
    procesada_regional = models.BooleanField(default=False)

    def __str__(self):
        return self.numero

class VotacionPresidenteRegional(models.Model):
    partido = models.ForeignKey(Partido)
    region = models.ForeignKey(Region)
    votos = models.IntegerField(default=0)
    
    def __str__(self):
        return "%s - %s" % (self.partido, self.region)

class VotacionConsejeroRegional(models.Model):
    partido = models.ForeignKey(Partido)
    provincia = models.ForeignKey(Provincia)
    votos = models.IntegerField(default=0)
    
    def __str__(self):
        return "%s - %s" % (self.partido, self.region)

class VotacionProvincial(models.Model):
    partido = models.ForeignKey(Partido)
    provincia = models.ForeignKey(Provincia)
    votos = models.IntegerField(default=0)
    
    def __str__(self):
        return "%s - %s" % (self.partido, self.provincia)

class VotacionDistrital(models.Model):
    partido = models.ForeignKey(Partido)
    distrito = models.ForeignKey(Distrito)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return "%s - %s" % (self.partido, self.distrito)
    
class ActaMunicipal(models.Model):
    mesa = models.OneToOneField(Mesa, primary_key=True)
    votos_blancos_prov = models.IntegerField()
    votos_blancos_dis = models.IntegerField()
    votos_nulos_prov = models.IntegerField()
    votos_nulos_dis = models.IntegerField()
    votos_impugnados_prov = models.IntegerField()
    votos_impugnados_dis = models.IntegerField()
    votos_emitidos_prov = models.IntegerField()
    votos_emitidos_dis = models.IntegerField()

    def votos_validos_prov(self):
        vvp = self.votos_emitidos_prov - self.votos_impugnados_prov - self.votos_nulos_prov - self.votos_blancos_prov
        return vvp

    def votos_validos_dis(self):
        vvd = self.votos_emitidos_dis - self.votos_impugnados_dis - self.votos_nulos_dis - self.votos_blancos_dis
        return vvd

    def __str__(self):
        return self.mesa.numero

class DetalleActaMunicipal(models.Model):
    acta = models.ForeignKey(ActaMunicipal)
    partido = models.ForeignKey(Partido)
    votos_provincial = models.IntegerField()
    votos_distrital = models.IntegerField()

    class Meta:
        unique_together = (('acta', 'partido'),)

    def __str__(self):
        return self.acta.mesa.numero+" "+self.partido.nombre

class ActaRegional(models.Model):
    mesa = models.OneToOneField(Mesa, primary_key=True)
    votos_blancos_pres = models.IntegerField()
    votos_nulos_pres = models.IntegerField()
    votos_impugnados_pres = models.IntegerField()
    votos_emitidos_pres = models.IntegerField()
    votos_blancos_cons = models.IntegerField()
    votos_nulos_cons = models.IntegerField()
    votos_impugnados_cons = models.IntegerField()
    votos_emitidos_cons = models.IntegerField()

    def votos_validos_pres(self):
        vvp = self.votos_emitidos_pres - self.votos_impugnados_pres - self.votos_nulos_pres - self.votos_blancos_pres
        return vvp

    def votos_validos_cons(self):
        vvc = self.votos_emitidos_cons - self.votos_impugnados_cons - self.votos_nulos_cons - self.votos_blancos_cons
        return vvc

    def __str__(self):
        return self.mesa.numero

class DetalleActaRegional(models.Model):
    acta = models.ForeignKey(ActaRegional)
    partido = models.ForeignKey(Partido)
    votos_pres = models.IntegerField()
    votos_cons = models.IntegerField()
    
    class Meta:
        unique_together = (('acta', 'partido'),)

    def __str__(self):
        return self.acta.mesa.numero+" "+self.partido.nombre

class DisenioActaMunicipal(models.Model):
    nombre = models.CharField(max_length=50)
    distrito = models.ForeignKey(Distrito)

    def __str__(self):
        return self.nombre

class DetalleDisenioActaMunicipal(models.Model):
    disenio_acta = models.ForeignKey(DisenioActaMunicipal)
    partido = models.ForeignKey(Partido)
    distrital = models.BooleanField(default=False)
    provincial = models.BooleanField(default=False)

    def __str__(self):
        return self.partido.nombre

class DisenioActaRegional(models.Model):
    nombre = models.CharField(max_length=50)
    region = models.ForeignKey(Region)

    def __str__(self):
        return self.nombre

class DetalleDisenioActaRegional(models.Model):
    disenio_acta = models.ForeignKey(DisenioActaRegional)
    partido = models.ForeignKey(Partido)
    presidente = models.BooleanField(default=False)
    consejero = models.BooleanField(default=False)

    def __str__(self):
        return self.partido.nombre