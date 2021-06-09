from django.db import models
from datetime import datetime


# TODO change the model name to person for example
class Person(models.Model):
    name = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    city = models.CharField(max_length=100)
    # what to show instead of usersobject(n)

    def __str__(self):
        return self.name
    # so in the administration its not Userss

    class Meta:
        verbose_name_plural = "Persones"


class Racine(models.Model):
    id_rac = models.BigAutoField(primary_key=True)
    rac = models.CharField(max_length=30)
    type_rac = models.IntegerField()

    def __str__(self):
        return self.rac


class Scheme(models.Model):
    id_sch = models.BigAutoField(primary_key=True)
    sch_cons = models.CharField(max_length=30)
    sch_voy = models.CharField(max_length=30)
    type_scheme = models.CharField(max_length=50)

    def __str__(self):
        return self.id_sch


class Verbe(models.Model):
    id_ver = models.BigAutoField(primary_key=True)
    ver_cons = models.CharField(max_length=30)
    ver_voy = models.CharField(max_length=30)
    scheme_ver = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    racine_ver = models.ForeignKey(Racine, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_ver


class Nom(models.Model):
    id_nom = models.BigAutoField(primary_key=True)
    nom_cons = models.CharField(max_length=30)
    nom_voy = models.CharField(max_length=30)
    scheme_nom = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    racine_nom = models.ForeignKey(Racine, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_ver
