from django.shortcuts import render, get_object_or_404 # Importe esta nova função
from .models import Item

def home(request):
    # ... (sua view home continua igual)
    itens = Item.objects.all()
    context = {
        'todos_os_itens': itens
    }
    return render(request, 'estoque/home.html', context)

# --- ADICIONE ESTA NOVA FUNÇÃO ---
def detalhe_item(request, pk): # Ponto crítico
    item = get_object_or_404(Item, pk=pk)
    context = {
        'item': item
    }
    return render(request, 'estoque/detalhe_item.html', context)

