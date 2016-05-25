from django import forms

class FormularioMesaNacional(forms.Form):
    mesas = forms.CharField(widget= forms.TextInput(attrs={'size': 100, 'class': 'form-control'}))  
    
class FormularioActaPresidencial(forms.Form):
    mesa = forms.CharField(widget = forms.HiddenInput())
    votos_blancos = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control numerico presidente','type': 'number','min': '0'}))
    votos_nulos = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control numerico presidente','type': 'number','min': '0'}))
    votos_impugnados = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control numerico presidente','type': 'number','min': '0'}))
    votos_totales = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control numerico total','type': 'number','min': '0','readonly': 'readonly'}))
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'cols': 141, 'rows': 5}))
    
class FormularioActaCongresal(forms.Form):
    mesa = forms.CharField(widget = forms.HiddenInput())
    votos_blancos = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control congresal','type': 'number','min': '0'}))
    votos_nulos = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control congresal','type': 'number','min': '0'}))
    votos_impugnados = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control congresal','type': 'number','min': '0'}))
    votos_totales = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control numerico','type': 'number','min': '0','readonly': 'readonly'}))
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'cols': 108, 'rows': 5}))