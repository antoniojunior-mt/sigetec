from django.urls import path
from . import views

app_name = 'estoque' # Ponto crítico 1

urlpatterns = [
    path('', views.home, name='home'),
    path('item/<int:pk>/', views.detalhe_item, name='detalhe_item'), # Ponto crítico 2
    path('item/<int:pk>/movimentar/', views.movimentar_item, name='movimentar_item'),
]
