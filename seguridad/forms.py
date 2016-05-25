# -*- coding: utf-8 -*- 
from django import forms 
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from seguridad.models import Perfil
import volpox.settings

lista_apps = [ app for app in volpox.settings.INSTALLED_APPS if not "django" in app ]
apps = zip(lista_apps, lista_apps)

class FormularioCambioPassword(forms.Form):
    password_actual = forms.CharField(widget=forms.PasswordInput)
    password_nueva = forms.CharField(widget=forms.PasswordInput)
    password_verificacion = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, usuario, *args, **kwargs):
        self.user = usuario
        super(FormularioCambioPassword, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    def clean_password_actual(self):
        if self.cleaned_data.get('password_actual') and not self.user.check_password(self.cleaned_data['password_actual']):
            raise ValidationError('La contraseña ingresada no es la actual.')
        return self.cleaned_data['password_actual']

    def clean_password_verificacion(self):
        if self.cleaned_data.get('password_nueva') and self.cleaned_data.get('password_verificacion') and self.cleaned_data['password_nueva'] != self.cleaned_data['password_verificacion']:
            raise ValidationError('Las contraseñas no coinciden')

class FormularioLogin(forms.Form):
    usuario = forms.CharField(label='Usuario',widget=forms.TextInput(attrs={'placeholder': 'usuario','class':'form-control'}))
    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={'placeholder': 'contraseña','class':'form-control'}))

    def clean_usuario(self):
        username = self.data['usuario']
        password = self.data['password']
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            if not usuario.is_active:
                raise ValidationError('Usuario no está activo')
        else:
            raise ValidationError('Error de Autenticación')
        return self.cleaned_data['usuario']
    
class FormularioPerfiles(forms.Form):
    perfil = forms.ModelChoiceField(queryset=Perfil.objects.all())
    aplicaciones = forms.ChoiceField(choices=apps, widget=forms.RadioSelect())