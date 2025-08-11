from django.urls import path
from . import views

app_name = 'estoque' # Ponto crítico 1

urlpatterns = [
    path('', views.home, name='home'),
    path('item/<int:pk>/', views.detalhe_item, name='detalhe_item'), # Ponto crítico 2
    path('item/<int:pk>/movimentar/', views.movimentar_item, name='movimentar_item'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/pdf/', views.relatorios_pdf, name='relatorios_pdf'),
    path('escolas/', views.lista_escolas, name='lista_escolas'),
    path('escolas/adicionar/', views.adicionar_escola, name='adicionar_escola'),
    
]
