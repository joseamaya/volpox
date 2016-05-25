# -*- encoding: utf-8 -*-
from django.db import models

class Region(models.Model):
    nombre = models.CharField(max_length=80)
   
    def __str__(self):
        return self.nombre    

class Provincia(models.Model):
    nombre = models.CharField(max_length=80)
    region = models.ForeignKey(Region)
    
    def __str__(self):
        return self.nombre    

class Distrito(models.Model):
    nombre = models.CharField(max_length=80)
    provincia = models.ForeignKey(Provincia)
    capital_provincia = models.BooleanField(default=None)

    def __str__(self):
        return self.nombre    

class CentroVotacion(models.Model):
    nombre = models.CharField(max_length=50)
    distrito = models.ForeignKey(Distrito)

    def __str__(self):
        return "%s - %s" % (self.nombre, self.distrito)
    
class Partido(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre