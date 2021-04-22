from django import forms
from .models import Users

class userForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = ['name','prenom','email','city']
    
         
    def clean(self):
        
        cleaned_data = super(userForm, self).clean()
        nom = cleaned_data.get('name')
        prenom = cleaned_data.get('prenom')
        email = cleaned_data.get('email')
        ville = cleaned_data.get('city')
        if not nom and not prenom and not ville and not email:
            raise forms.ValidationError('il faut ecrire quelque chose!')
  