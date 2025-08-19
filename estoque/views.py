from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Count, Max, Q, F
from django.utils import timezone
from datetime import timedelta

# Importando os novos modelos e formulários
from .models import Produto, Estoque, Escola, Movimentacao, Categoria, Fornecedor
from .forms import ProdutoForm, EntradaEstoqueForm, EscolaForm, MovimentacaoForm, RelatorioFiltroForm

# --- Páginas Principais e Listas ---

def home(request):
    # A nova página inicial (dashboard)
    total_produtos = Produto.objects.count()
    total_escolas = Escola.objects.count()
    context = {
        'total_produtos': total_produtos,
        'total_escolas': total_escolas,
    }
    return render(request, 'estoque/home.html', context)

def lista_produtos(request):
    # A antiga 'lista_itens' agora é 'lista_produtos'
    # Usamos .annotate() para calcular o estoque disponível para cada produto
    produtos = Produto.objects.annotate(
        estoque_disponivel=Sum('estoque__quantidade') - Sum('movimentacao__quantidade', filter=Q(movimentacao__tipo='SAIDA'))
    ).order_by('nome')

    context = {
        'produtos': produtos
    }
    return render(request, 'estoque/lista_produtos.html', context)

def detalhe_produto(request, pk):
    # O antigo 'detalhe_item' agora é 'detalhe_produto'
    produto = get_object_or_404(Produto, pk=pk)
    estoque_disponivel = Estoque.objects.filter(produto=produto).aggregate(total=Sum('quantidade'))['total'] or 0
    saidas = Movimentacao.objects.filter(produto=produto, tipo='SAIDA').aggregate(total=Sum('quantidade'))['total'] or 0

    context = {
        'produto': produto,
        'estoque_disponivel': estoque_disponivel - saidas,
        'historico_entradas': Estoque.objects.filter(produto=produto).order_by('-data_entrada'),
        'historico_saidas': Movimentacao.objects.filter(produto=produto, tipo='SAIDA').order_by('-data'),
    }
    return render(request, 'estoque/detalhe_produto.html', context)

def lista_escolas(request):
    escolas = Escola.objects.all().order_by('nome')
    context = { 'escolas': escolas }
    return render(request, 'estoque/lista_escolas.html', context)

# --- Formulários e Ações ---

def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo produto cadastrado com sucesso!')
            return redirect('estoque:lista_produtos')
    else:
        form = ProdutoForm()

    context = { 'form': form }
    return render(request, 'estoque/adicionar_produto.html', context)

def entrada_estoque(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = EntradaEstoqueForm(request.POST)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.produto = produto
            entrada.save()
            messages.success(request, f"Entrada de {entrada.quantidade}x '{produto.nome}' registrada com sucesso!")
            return redirect('estoque:detalhe_produto', pk=produto.pk)
    else:
        form = EntradaEstoqueForm()

    context = { 'form': form, 'produto': produto }
    return render(request, 'estoque/entrada_estoque.html', context)

def movimentar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    estoque_disponivel = Estoque.objects.filter(produto=produto).aggregate(total=Sum('quantidade'))['total'] or 0
    saidas = Movimentacao.objects.filter(produto=produto, tipo='SAIDA').aggregate(total=Sum('quantidade'))['total'] or 0
    estoque_real = estoque_disponivel - saidas

    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)

            if movimentacao.quantidade > estoque_real:
                messages.error(request, f"Erro: A quantidade de saída ({movimentacao.quantidade}) é maior que a disponível ({estoque_real}).")
                return redirect('estoque:movimentar_produto', pk=produto.pk)

            movimentacao.produto = produto
            movimentacao.save()
            messages.success(request, 'Movimentação registrada com sucesso!')
            return redirect('estoque:detalhe_produto', pk=produto.pk)
    else:
        form = MovimentacaoForm()

    context = {
        'form': form,
        'produto': produto,
        'estoque_disponivel': estoque_real,
    }
    return render(request, 'estoque/movimentar_produto.html', context)

def adicionar_escola(request):
    if request.method == 'POST':
        form = EscolaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova escola cadastrada com sucesso!')
            return redirect('estoque:lista_escolas')
    else:
        form = EscolaForm()

    context = { 'form': form }
    return render(request, 'estoque/adicionar_escola.html', context)

# --- Relatórios ---

def relatorios(request):
    form = RelatorioFiltroForm(request.GET)
    movimentacoes_saida = Movimentacao.objects.filter(tipo='SAIDA')
    if form.is_valid():
        periodo = form.cleaned_data.get('periodo')
        produto_selecionado = form.cleaned_data.get('produto')
        if periodo and periodo != 'todos':
            dias = int(periodo)
            data_limite = timezone.now() - timedelta(days=dias)
            movimentacoes_saida = movimentacoes_saida.filter(data__gte=data_limite)
        if produto_selecionado:
            movimentacoes_saida = movimentacoes_saida.filter(produto=produto_selecionado)

    relatorio_periodo = movimentacoes_saida.values(
        'escola__nome', 'produto__nome'
    ).annotate(total_quantidade=Sum('quantidade')).order_by('escola__nome', 'produto__nome')

    relatorio_por_produto = Produto.objects.filter(
        id__in=movimentacoes_saida.values_list('produto_id', flat=True).distinct()
    ).annotate(
        total_saida=Sum('movimentacao__quantidade', filter=Q(movimentacao__in=movimentacoes_saida)),
        escola_que_mais_recebeu=Max('movimentacao__escola__nome', filter=Q(movimentacao__in=movimentacoes_saida))
    ).order_by('-total_saida')

    context = {
        'form': form,
        'relatorio_periodo': relatorio_periodo,
        'relatorio_por_produto': relatorio_por_produto,
    }
    return render(request, 'estoque/relatorios.html', context)

def relatorios_pdf(request):
    # Esta função também precisaria de ajustes, mas vamos focar em fazer o site funcionar primeiro.
    # Por enquanto, vamos deixar uma versão simples.
    return HttpResponse("Página de PDF em construção.")