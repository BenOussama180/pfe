from unicodedata import lookup
import django
from django.db.models import fields
from django.db.models.fields import BigAutoField
from django.db.models.fields.related import ForeignKey
import django_filters
from django_filters import *
from dns.resolver import Cache
from .models import Person, Scheme, Verbe, Racine, Nom


class PersonFilter(django_filters.FilterSet):
    id = CharFilter(field_name="id", lookup_expr='iexact')
    name = CharFilter(field_name="name", lookup_expr='icontains')
    prenom = CharFilter(field_name="prenom", lookup_expr='icontains')
    city = CharFilter(field_name="city", lookup_expr='icontains')

    class Meta:
        model = Person
        fields = '__all__'
        exclude = ['name', 'prenom', 'city', 'email', 'created_at']

##############


class VerbeFilter(django_filters.FilterSet):
    id_ver = CharFilter(field_name="id_ver", lookup_expr='iexact')
    verbe = CharFilter(field_name="verbe", lookup_expr='icontains')
    ver_cons = CharFilter(field_name="ver_cons", lookup_expr='icontains')
    ver_voy = CharFilter(field_name="ver_voy", lookup_expr='icontains')

    class Meta:
        model = Verbe
        fields = '__all__'
        exclude = ['id_ver', 'verbe', 'ver_cons', 'ver_voy']


class NomFilter(django_filters.FilterSet):
    id_nom = CharFilter(field_name="id_nom", lookup_expr='iexact')
    nom = CharFilter(field_name="nom", lookup_expr='icontains')
    nom_cons = CharFilter(field_name="nom_voy", lookup_expr='icontains')
    nom_voy = CharFilter(field_name="nom_voy", lookup_expr='icontains')

    class Meta:
        model = Nom
        fields = '__all__'
        exclude = ['id_nom', 'nom', 'nom_cons', 'nom_voy']


class RacineFilter(django_filters.FilterSet):
    id_rac = CharFilter(field_name="id_rac", lookup_expr='iexact')

    class Meta:
        model = Racine
        fields = '__all__'


class SchemeFilter(django_filters.FilterSet):
    id_sch = CharFilter(field_name="id_sch", lookup_expr='iexact')

    class Meta:
        model = Scheme
        fields = '__all__'
