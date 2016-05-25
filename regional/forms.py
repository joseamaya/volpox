from django import forms

class FormularioMesa(forms.Form):
    mesas = forms.CharField(widget= forms.TextInput(attrs={'size': 100, 'class': 'form-control'}))  
    
class FormularioActaRegional(forms.Form):
    voto_blanco_pres = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control','class': 'presidente','type': 'number'}))
    voto_nulo_pres = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control','class': 'presidente','type': 'number'}))
    voto_impugnado_pres = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control','class': 'presidente','type': 'number'}))
    voto_total_pres = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control','class': 'presidente','type': 'number'}))
    voto_blanco_cons = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control','class': 'consejero','type': 'number'}))
    voto_nulo_cons = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control','class': 'consejero','type': 'number'}))
    voto_impugnado_cons = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control','class': 'consejero','type': 'number'}))
    voto_total_cons = forms.CharField(widget= forms.TextInput(attrs={'size': 20, 'class': 'form-control','class': 'consejero','type': 'number'}))
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'cols': 146, 'rows': 5}))