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

    class Meta:
        verbose_name_plural = "Persones"

#################


class Racine(models.Model):
    id_rac = models.BigAutoField(primary_key=True)
    rac = models.CharField(max_length=30)
    type_rac = models.IntegerField()
    classe_rac = models.CharField(max_length=100)

    def __str__(self):
        return self.rac


class Scheme(models.Model):

    NOMBRE_CHOICES = [
        ('مفرد', 'مفرد'),
        ('مثنى', 'مثنى'),
        ('جمع', 'جمع'),
    ]
    UNIT_CHOICES = [
        ('مذكر', 'مفرد'),
        ('مؤنث', 'مثنى'),
        ('مذكر\مؤنث', 'مذكر\مؤنث'),
    ]
    ORA_CHOICES = [
        ('متكلم', 'متكلم'),
        ('مخاطب', 'مخاطب'),
        ('غائب', 'غائب'),
    ]
    CONJ_CHOICES = [
        ('ماضي', 'ماضي'),
        ('حاظر', 'حاظر'),
        ('أمر', 'أمر'),
    ]
    TYP_CHOICES = [
        ('فعل', 'فعل'),
        ('اسم', 'اسم'),
        ('اسم/نعت', 'اسم/نعت'),
    ]

    id_sch = models.BigAutoField(primary_key=True)
    sch_cons = models.CharField(max_length=30)
    sch_voy = models.CharField(max_length=30)
    scheme = models.CharField(max_length=50, null=True)
    type_scheme = models.IntegerField()
    classe_sch = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100, choices=NOMBRE_CHOICES)
    unit = models.CharField(max_length=100, choices=UNIT_CHOICES)
    ora = models.CharField(max_length=100, choices=ORA_CHOICES)
    conj = models.CharField(max_length=100, choices=CONJ_CHOICES)
    typ = models.CharField(max_length=100, choices=TYP_CHOICES, null=True)

    def __str__(self):
        return self.scheme


class Verbe(models.Model):
    id_ver = models.BigAutoField(primary_key=True)
    verbe = models.CharField(max_length=80, null=True)
    ver_cons = models.CharField(max_length=30)
    ver_voy = models.CharField(max_length=30)
    scheme_ver = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    racine_ver = models.ForeignKey(Racine, on_delete=models.CASCADE)

    def __str__(self):
        return self.verbe


class Nom(models.Model):
    id_nom = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=80, null=True)
    nom_cons = models.CharField(max_length=30)
    nom_voy = models.CharField(max_length=30)
    scheme_nom = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    racine_nom = models.ForeignKey(Racine, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom
