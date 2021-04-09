from django import forms
from .models import Users

class userForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = ['name','email','city']
  