from django import forms
from .models import Vaga

class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['nome', 'requisitos', 'faixa_salarial', 'escolaridade_minima']