import django_filters
from django_filters import DateFilter, CharFilter
from .models import Person

class PersonFilter(django_filters.FilterSet):
    id = CharFilter(field_name="id",lookup_expr='iexact')
    name = CharFilter(field_name="name",lookup_expr='icontains')
    prenom = CharFilter(field_name="prenom",lookup_expr='icontains')
    city = CharFilter(field_name="city",lookup_expr='icontains')
    
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ['name','prenom','city','email','created_at']

    # adding css to inputs not working for now
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)  
    #     self.fields["id"].widgets.attrs.update({"class": "form-control mb-2 account-form"})
    #     self.fields["name"].widgets.attrs.update({"class": "form-control mb-2 account-form"})
    #     self.fields["prenom"].widgets.attrs.update({"class": "form-control mb-2 account-form"})
    #     self.fields["city"].widgets.attrs.update({"class": "form-control mb-2 account-form"})

    
        