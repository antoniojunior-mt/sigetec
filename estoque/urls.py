from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.home, name='home'),
    path('itens/', views.lista_itens, name='lista_itens'),
    path('itens/adicionar/', views.adicionar_item, name='adicionar_item'),
    path('item/<int:pk>/', views.detalhe_item, name='detalhe_item'),
    path('item/<int:pk>/movimentar/', views.movimentar_item, name='movimentar_item'),
    path('escolas/', views.lista_escolas, name='lista_escolas'),
    path('escolas/adicionar/', views.adicionar_escola, name='adicionar_escola'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/pdf/', views.relatorios_pdf, name='relatorios_pdf'),
]