from django.db import models
from django.utils import timezone

# NOVO MODELO: Categoria
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nome'] # Ordena as categorias por nome

    def __str__(self):
        return self.nome

# NOVO MODELO: Fornecedor (sem alterações)
class Fornecedor(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Fornecedor")

    def __str__(self):
        return self.nome

# NOVO MODELO: Produto (o nosso antigo "Item")
class Produto(models.Model):
    nome = models.CharField(max_length=200, unique=True, verbose_name="Nome do Produto")
    descricao = models.TextField(verbose_name="Descrição", null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name="Categoria")

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

# MODELO 'Item' RENOMEADO E TRANSFORMADO EM 'Estoque'
class Estoque(models.Model):
    # Ligação com o catálogo de produtos
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
    quantidade = models.PositiveIntegerField()
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço de Custo")
    data_entrada = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Lote de {self.quantidade}x {self.produto.nome} (Fornecedor: {self.fornecedor.nome if self.fornecedor else 'N/A'})"

# MODELO 'Escola' (sem alterações)
class Escola(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome da Escola")
    endereco = models.TextField(verbose_name="Endereço", null=True, blank=True)

    def __str__(self):
        return self.nome

# MODELO 'Movimentacao' (PRECISA SER ATUALIZADO)
class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('SAIDA', 'Saída para Escola'),
        ('ENTRADA', 'Entrada no Estoque'), # Manteremos isso para o histórico
    ]

    # AGORA a movimentação é de um PRODUTO, não de um Lote de Estoque.
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, verbose_name="Produto")
    escola = models.ForeignKey(Escola, on_delete=models.PROTECT, verbose_name="Escola")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo de Movimentação")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade Movimentada")
    data = models.DateTimeField(default=timezone.now, verbose_name="Data da Movimentação")

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.quantidade}x {self.produto.nome}"
    