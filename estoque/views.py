from django.shortcuts import render, get_object_or_404, redirect # Adicione redirect
from django.contrib import messages # Para mostrar mensagens ao usuário
from django.db import transaction # Para garantir a segurança da transação
from .forms import MovimentacaoForm, EscolaForm, RelatorioFiltroForm # Importe nosso novo formulário
from .models import Item, Movimentacao, Escola
from django.db.models import Sum, Count, Max, F, Q
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

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

def relatorios(request):
    # Inicializa o formulário de filtro
    form = RelatorioFiltroForm(request.GET)

    # Base da consulta: apenas movimentações de SAÍDA
    movimentacoes_saida = Movimentacao.objects.filter(tipo='SAIDA')

    # --- Filtros ---
    if form.is_valid():
        periodo = form.cleaned_data.get('periodo')
        item_selecionado = form.cleaned_data.get('item')

        if periodo and periodo != 'todos':
            dias = int(periodo)
            data_limite = timezone.now() - timedelta(days=dias)
            movimentacoes_saida = movimentacoes_saida.filter(data__gte=data_limite)

        if item_selecionado:
            movimentacoes_saida = movimentacoes_saida.filter(item=item_selecionado)

    # --- Relatório 1: Movimentação por Período (Mensal/Anual) ---
    # Agrupa por escola e por item, e soma as quantidades.
    relatorio_periodo = movimentacoes_saida.values(
        'escola__nome', 'item__nome'
    ).annotate(
        total_quantidade=Sum('quantidade')
    ).order_by('escola__nome', 'item__nome')

    # --- Relatório 2: Movimentação por Item ---
    # Agrupa por item e calcula o total que saiu e a escola que mais recebeu.
    relatorio_por_item = Item.objects.filter(
        # Apenas itens que tiveram movimentação de saída
        id__in=movimentacoes_saida.values_list('item_id', flat=True).distinct()
    ).annotate(
        # Soma a quantidade total de saída para cada item
        # A correção está aqui: trocamos F() por Q()
        total_saida=Sum('movimentacao__quantidade', filter=Q(movimentacao__in=movimentacoes_saida)),
        # Encontra a escola que mais recebeu
        # E aqui também: trocamos F() por Q()
        escola_que_mais_recebeu=Max('movimentacao__escola__nome', filter=Q(movimentacao__in=movimentacoes_saida))
    ).order_by('-total_saida')

    context = {
        'form': form,
        'relatorio_periodo': relatorio_periodo,
        'relatorio_por_item': relatorio_por_item,
    }
    return render(request, 'estoque/relatorios.html', context)

def lista_escolas(request):
    escolas = Escola.objects.all().order_by('nome')
    context = {
        'escolas': escolas
    }
    return render(request, 'estoque/lista_escolas.html', context)

# View para adicionar uma nova escola
def adicionar_escola(request):
    if request.method == 'POST':
        form = EscolaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova escola cadastrada com sucesso!')
            return redirect('estoque:lista_escolas')
    else:
        form = EscolaForm()

    context = {
        'form': form
    }
    return render(request, 'estoque/adicionar_escola.html', context)

def relatorios_pdf(request):
    # A lógica para buscar e filtrar os dados é EXATAMENTE A MESMA da view de relatórios
    form = RelatorioFiltroForm(request.GET)
    movimentacoes_saida = Movimentacao.objects.filter(tipo='SAIDA')
    if form.is_valid():
        periodo = form.cleaned_data.get('periodo')
        item_selecionado = form.cleaned_data.get('item')
        if periodo and periodo != 'todos':
            dias = int(periodo)
            data_limite = timezone.now() - timedelta(days=dias)
            movimentacoes_saida = movimentacoes_saida.filter(data__gte=data_limite)
        if item_selecionado:
            movimentacoes_saida = movimentacoes_saida.filter(item=item_selecionado)

    relatorio_periodo = movimentacoes_saida.values(
        'escola__nome', 'item__nome'
    ).annotate(total_quantidade=Sum('quantidade')).order_by('escola__nome', 'item__nome')

    relatorio_por_item = Item.objects.filter(
        id__in=movimentacoes_saida.values_list('item_id', flat=True).distinct()
    ).annotate(
        total_saida=Sum('movimentacao__quantidade', filter=Q(movimentacao__in=movimentacoes_saida)),
        escola_que_mais_recebeu=Max('movimentacao__escola__nome', filter=Q(movimentacao__in=movimentacoes_saida))
    ).order_by('-total_saida')

    context = {
        'relatorio_periodo': relatorio_periodo,
        'relatorio_por_item': relatorio_por_item,
    }

    # --- A MÁGICA DO PDF ACONTECE AQUI ---
    # 1. Renderiza o template HTML como uma string
    html_string = render_to_string('estoque/relatorio_pdf_template.html', context)

    # 2. Converte a string HTML para PDF usando WeasyPrint
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # 3. Cria uma resposta HTTP com o PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_estoque.pdf"' # Força o download
    return response
