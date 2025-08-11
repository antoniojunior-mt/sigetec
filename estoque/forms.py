from django import forms
from .models import Movimentacao

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        # Campos que aparecerão no formulário para o usuário
        fields = ['escola', 'quantidade', 'tipo']
        