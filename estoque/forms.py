from django import forms
from .models import Movimentacao, Escola, Fornecedor, Produto, Categoria, Estoque

# --- FORMULÁRIO PARA CRIAR/EDITAR UM PRODUTO ---
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'categoria']

# --- FORMULÁRIO PARA DAR ENTRADA DE ESTOQUE DE UM PRODUTO ---
class EntradaEstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        # O usuário informará o fornecedor, a quantidade e o preço de custo.
        # O 'produto' será definido pela view, a partir da URL.
        fields = ['fornecedor', 'quantidade', 'preco_custo']

# --- FORMULÁRIOS QUE JÁ TINHAMOS (ATUALIZADOS SE NECESSÁRIO) ---

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = ['nome', 'endereco']

# O MovimentacaoForm agora se refere a 'produto' em vez de 'item'
class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['escola', 'quantidade', 'tipo']

# O RelatorioFiltroForm agora filtra por 'Produto'
class RelatorioFiltroForm(forms.Form):
    PERIODO_CHOICES = [
        ('30', 'Últimos 30 dias'),
        ('365', 'Último ano'),
        ('todos', 'Desde o início'),
    ]
    periodo = forms.ChoiceField(choices=PERIODO_CHOICES, label="Período de Análise", required=False)
    produto = forms.ModelChoiceField( # Mudamos de 'item' para 'produto'
        queryset=Produto.objects.all(), 
        required=False, 
        label="Produto Específico",
        empty_label="-- Todos os Produtos --"
    )