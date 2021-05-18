from unicodedata import name
from django import forms
from .models import Person


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['name', 'prenom', 'email', 'city']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     name = cleaned_data.get('name')
    #     prenom = cleaned_data.get('prenom')
    #     email = cleaned_data.get('email')
    #     ville = cleaned_data.get('city')
    #     if not name and not prenom and not ville and not email:
    #         raise forms.ValidationError('il faut ecrire quelque chose!')
