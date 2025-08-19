from django.contrib import admin
from .models import Categoria, Fornecedor, Produto, Estoque, Escola, Movimentacao

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'descricao')
    list_filter = ('categoria',)
    search_fields = ('nome',)

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto', 'fornecedor', 'quantidade', 'data_entrada')
    list_filter = ('fornecedor', 'data_entrada')
    search_fields = ('produto__nome',)

@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco')
    search_fields = ('nome',)

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'escola', 'tipo', 'quantidade', 'data')
    list_filter = ('tipo', 'escola', 'data')
    search_fields = ('produto__nome',)