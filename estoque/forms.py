from django import forms
from .models import Movimentacao, Escola, Item, Fornecedor

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        # Campos que aparecerão no formulário para o usuário
        fields = ['escola', 'quantidade', 'tipo']

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = ['nome']

class RelatorioFiltroForm(forms.Form):
    PERIODO_CHOICES = [
        ('30', 'Últimos 30 dias'),
        ('365', 'Último ano'),
        ('todos', 'Desde o início'),
    ]

    periodo = forms.ChoiceField(choices=PERIODO_CHOICES, label="Período de Análise", required=False)

    # 'queryset' busca todos os itens. 'required=False' torna a seleção opcional.
    # 'empty_label' é o texto que aparece para a opção "todos os itens".
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(), 
        required=False, 
        label="Item Específico",
        empty_label="-- Todos os Itens --"
    )

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        # quantidade_disponivel será igual à total no cadastro
        fields = ['nome', 'descricao', 'fornecedor', 'quantidade_total']
                