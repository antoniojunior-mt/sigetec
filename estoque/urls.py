from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    # --- URLs Principais e de Listagem ---
    path('', views.home, name='home'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('escolas/', views.lista_escolas, name='lista_escolas'),

    # --- URLs para Detalhes ---
    path('produto/<int:pk>/', views.detalhe_produto, name='detalhe_produto'),

    # --- URLs para Adicionar (Formulários) ---
    path('produtos/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('escolas/adicionar/', views.adicionar_escola, name='adicionar_escola'),
    path('produto/<int:pk>/entrada/', views.entrada_estoque, name='entrada_estoque'),

    # --- URLs para Ações ---
    path('produto/<int:pk>/movimentar/', views.movimentar_produto, name='movimentar_produto'),

    # --- URLs de Relatórios ---
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/pdf/', views.relatorios_pdf, name='relatorios_pdf'),
]
