from django.contrib import admin
from django.urls import path, include # Adicione 'include' aqui

urlpatterns = [
    path('admin/', admin.site.urls),
    # Adicione esta linha:
    path('', include('estoque.urls')), # Diz ao projeto para usar as URLs do app estoque
]
