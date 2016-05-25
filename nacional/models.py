from django.db import models
from localizacion.models import CentroVotacion, Partido, Region
from django.db.models import Sum

# Create your models here.
class MesaNacional(models.Model):
    numero = models.CharField(max_length=6, primary_key=True)
    total_electores = models.IntegerField()
    centro_votacion = models.ForeignKey(CentroVotacion)
    procesada_presidencial = models.BooleanField(default=False)
    procesada_congresal = models.BooleanField(default=False)
    procesada_parlandino = models.BooleanField(default=False)

    def __str__(self):
        return self.numero
    
class ActaPresidencial(models.Model):
    mesa = models.ForeignKey(MesaNacional, primary_key=True)
    votos_blancos = models.IntegerField()
    votos_nulos = models.IntegerField()
    votos_impugnados = models.IntegerField()
    votos_emitidos = models.IntegerField()    

    def votos_validos(self):
        vvp = self.votos_emitidos - self.votos_impugnados - self.votos_nulos - self.votos_blancos
        return vvp

    def __str__(self):
        return self.mesa.numero
    
class DetalleActaPresidencial(models.Model):
    acta = models.ForeignKey(ActaPresidencial)
    partido = models.ForeignKey(Partido)
    votos = models.IntegerField()    
    
    class Meta:
        unique_together = (('acta', 'partido'),)

    def __str__(self):
        return self.acta.mesa.numero+" "+self.partido.nombre
    
class DisenioActaPresidencial(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

class DetalleDisenioActaPresidencial(models.Model):
    disenio_acta = models.ForeignKey(DisenioActaPresidencial)
    partido = models.ForeignKey(Partido)
    presidente = models.BooleanField(default=False)    

    def __str__(self):
        return self.partido.nombre
    
class VotacionPresidente(models.Model):
    partido = models.ForeignKey(Partido)
    votos = models.IntegerField(default=0)
    
    def __str__(self):
        return "%s - %s" % (self.partido)
    
    def porcentaje(self):
        total = VotacionPresidente.objects.all().aggregate(Sum('votos'))
        return round(self.votos*100.00/total['votos__sum'],2)
    
class DisenioActaCongresal(models.Model):
    nombre = models.CharField(max_length=50)
    region = models.ForeignKey(Region)

    def __str__(self):
        return self.nombre

class DetalleDisenioActaCongresal(models.Model):
    disenio_acta = models.ForeignKey(DisenioActaCongresal)
    partido = models.ForeignKey(Partido)
    numero1 = models.BooleanField(default=False)
    numero2 = models.BooleanField(default=False)
    numero3 = models.BooleanField(default=False)
    numero4 = models.BooleanField(default=False)
    numero5 = models.BooleanField(default=False)
    numero6 = models.BooleanField(default=False)
    numero7 = models.BooleanField(default=False)
    numero8 = models.BooleanField(default=False)
    numero9 = models.BooleanField(default=False)
    numero10 = models.BooleanField(default=False)
    numero11 = models.BooleanField(default=False)
    numero12 = models.BooleanField(default=False)
    numero13 = models.BooleanField(default=False)
    numero14 = models.BooleanField(default=False)
    numero15 = models.BooleanField(default=False)
    numero16 = models.BooleanField(default=False)
    numero17 = models.BooleanField(default=False)
    numero18 = models.BooleanField(default=False)
    numero19 = models.BooleanField(default=False)
    numero20 = models.BooleanField(default=False)
    numero21 = models.BooleanField(default=False)
    numero22 = models.BooleanField(default=False)
    numero23 = models.BooleanField(default=False)
    numero24 = models.BooleanField(default=False)
    numero25 = models.BooleanField(default=False)
    numero26 = models.BooleanField(default=False)
    numero27 = models.BooleanField(default=False)
    numero28 = models.BooleanField(default=False)
    numero29 = models.BooleanField(default=False)
    numero30 = models.BooleanField(default=False)
    numero31 = models.BooleanField(default=False)
    numero32 = models.BooleanField(default=False)
    numero33 = models.BooleanField(default=False)
    numero34 = models.BooleanField(default=False)
    numero35 = models.BooleanField(default=False)
    numero36 = models.BooleanField(default=False)  
    
class ActaCongresal(models.Model):
    mesa = models.ForeignKey(MesaNacional, primary_key=True)
    votos_blancos = models.IntegerField()
    votos_nulos = models.IntegerField()
    votos_impugnados = models.IntegerField()
    votos_emitidos = models.IntegerField()    

    def votos_validos(self):
        vvp = self.votos_emitidos - self.votos_impugnados - self.votos_nulos - self.votos_blancos
        return vvp

    def __str__(self):
        return self.mesa.numero

class DetalleActaCongresal(models.Model):
    acta = models.ForeignKey(ActaCongresal)
    partido = models.ForeignKey(Partido)
    numero = models.IntegerField()
    votos = models.IntegerField()    
    
    class Meta:
        unique_together = (('acta', 'partido', 'numero'),)

    def __str__(self):
        return self.acta.mesa.numero+" "+self.partido.nombre
    
class VotacionCongresalCandidato(models.Model):
    partido = models.ForeignKey(Partido)
    region = models.ForeignKey(Region)
    numero = models.IntegerField()
    votos = models.IntegerField(default=0)    
    
    def __str__(self):
        return "%s - %s - %s" % (self.partido, self.region,self.numero)
    
class VotacionCongresalTotal(models.Model):
    partido = models.ForeignKey(Partido)
    region = models.ForeignKey(Region)
    votos = models.IntegerField(default=0)    
    
    def __str__(self):
        return "%s - %s - %s" % (self.partido, self.region)