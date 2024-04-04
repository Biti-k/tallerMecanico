from django import forms
from django.forms import ModelChoiceField, ChoiceField
from . import models

class LoginForm(forms.Form):
    usuario = forms.CharField(label="Usuario", max_length=12, required=True, label_suffix='')
    password = forms.CharField(required=True, label="Contraseña", label_suffix='', widget=forms.PasswordInput)
    
class CrearReparacionForm(forms.Form):
    choices = (("-1", "---------"))
    cliente = ModelChoiceField(queryset=models.Cliente.objects.all(), required=True, label_suffix='', label='Cliente', widget=forms.Select(attrs={'id': 'clientesSelect'}))
    coche = ChoiceField(required=True, label_suffix='', label='Coche', widget=forms.Select(attrs={'id': 'cochesSelect'}))
    
class CocheNuevo(forms.Form):
    matricula = forms.CharField(label="Matrícula", max_length=7, required=True, label_suffix='')
    km = forms.IntegerField(label="Kilometraje", required=True, label_suffix='',min_value=0)
