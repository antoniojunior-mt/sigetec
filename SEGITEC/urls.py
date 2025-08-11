from django.contrib import admin
from django.urls import path, include # Ponto crítico 1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('estoque.urls')), # Ponto crítico 2
]