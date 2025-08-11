from django.shortcuts import render, get_object_or_404, redirect # Adicione redirect
from django.contrib import messages # Para mostrar mensagens ao usuário
from django.db import transaction # Para garantir a segurança da transação
from .models import Item
from .forms import MovimentacaoForm # Importe nosso novo formulário

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

def movimentar_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        # Se o formulário foi enviado (requisição POST)
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            try:
                # 'with transaction.atomic()' garante que as duas operações 
                # (criar movimentação e atualizar item) aconteçam com sucesso, ou nenhuma acontece.
                # Isso previne inconsistência no banco de dados.
                with transaction.atomic():
                    # Pega os dados do formulário mas não salva no banco ainda
                    movimentacao = form.save(commit=False)

                    # Validação de negócio: a quantidade a ser retirada não pode ser maior que a disponível
                    if movimentacao.quantidade > item.quantidade_disponivel:
                        messages.error(request, f"Erro: A quantidade de saída ({movimentacao.quantidade}) é maior que a disponível ({item.quantidade_disponivel}).")
                        # Se der erro, redireciona de volta para o formulário sem fazer nada.
                        return redirect('estoque:movimentar_item', pk=item.pk)

                    # Define o item da movimentação (que veio da URL)
                    movimentacao.item = item
                    movimentacao.save() # Agora sim, salva a movimentação

                    # Atualiza a quantidade do item e salva
                    item.quantidade_disponivel -= movimentacao.quantidade
                    item.save()

                # Mostra uma mensagem de sucesso
                messages.success(request, 'Movimentação registrada com sucesso!')
                # Redireciona para a página de detalhes do item
                return redirect('estoque:detalhe_item', pk=item.pk)

            except Exception as e:
                messages.error(request, f"Ocorreu um erro inesperado: {e}")

    else:
        # Se a página foi apenas carregada (requisição GET)
        form = MovimentacaoForm()

    context = {
        'form': form,
        'item': item
    }
    return render(request, 'estoque/movimentar_item.html', context)
