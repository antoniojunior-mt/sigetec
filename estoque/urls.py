from django.urls import path
from . import views # Importa as views do app atual

app_name = 'estoque' # Boa prática para organizar as URLs

urlpatterns = [
    # Quando o usuário acessar a URL raiz do app, chame a função 'home' da views.py
    path('', views.home, name='home'),
]