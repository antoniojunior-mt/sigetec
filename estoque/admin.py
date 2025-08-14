from django.contrib import admin
from .models import Escola, Item, Fornecedor, Movimentacao

@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco')
    search_fields = ('nome',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade_disponivel', 'quantidade_total')
    search_fields = ('nome',)

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('item', 'escola', 'tipo', 'quantidade', 'data')
    list_filter = ('tipo', 'escola', 'data') # Adiciona filtros na lateral
    autocomplete_fields = ('item', 'escola') # Melhora a seleção de item e escola
    