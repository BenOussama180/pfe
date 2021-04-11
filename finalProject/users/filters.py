import django_filters
from django_filters import DateFilter, CharFilter
from .models import Users

class userFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name",lookup_expr='icontains')
    prenom = CharFilter(field_name="prenom",lookup_expr='icontains')
    city = CharFilter(field_name="city",lookup_expr='icontains')
    
    class Meta:
        model = Users
        fields = '__all__'
        exclude = ['name','prenom','city','email','created_at']