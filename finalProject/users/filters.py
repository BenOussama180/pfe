import django_filters
from django_filters import DateFilter, CharFilter
from .models import Users

class userFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name",lookup_expr='icontains')
    city = CharFilter(field_name="city",lookup_expr='icontains')
    
    class Meta:
        model = Users
        fields = '__all__'
        exclude = ['name','city','email','created_at']