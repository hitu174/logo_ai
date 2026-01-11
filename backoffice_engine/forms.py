from django import forms
from backoffice_engine.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["name","mobile_number","email","password"]
class UserUpdate(forms.ModelForm):
    class Meta:
        model=User
        fields=["name","mobile_number","password"]     