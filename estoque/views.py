from django.shortcuts import render
from .models import Item # Importamos nosso modelo de Item

# Create your views here.

def home(request):
    # 1. Buscar todos os itens do banco de dados
    itens = Item.objects.all()

    # 2. Criar um "contexto" para enviar os dados para o template
    context = {
        'todos_os_itens': itens
    }

    # 3. Renderizar o template HTML, passando os dados do contexto
    return render(request, 'estoque/home.html', context)
