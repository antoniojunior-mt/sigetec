from django.db import models
from django.utils import timezone # Vamos usar para a data

# Create your models here.

# Tabela ESCOLAS
class Escola(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome da Escola")
    endereco = models.TextField(verbose_name="Endereço", null=True, blank=True)

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Fornecedor")

    def __str__(self):
        return self.nome

# Tabela ITENS
class Item(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Item")
    descricao = models.TextField(verbose_name="Descrição", null=True, blank=True)
    # --- ADICIONE ESTA LINHA ---
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fornecedor")

    quantidade_total = models.PositiveIntegerField(verbose_name="Quantidade Total em Estoque")
    quantidade_disponivel = models.PositiveIntegerField(verbose_name="Quantidade Disponível")

    def __str__(self):
        return f"{self.nome} (Disponível: {self.quantidade_disponivel})"


# Tabela MOVIMENTACAO
class Movimentacao(models.Model):
    
    # Opções para o campo 'tipo'
    TIPO_CHOICES = [
        ('SAIDA', 'Saída para Escola'),
        ('ENTRADA', 'Entrada no Estoque'),
    ]

    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name="Item")
    escola = models.ForeignKey(Escola, on_delete=models.PROTECT, verbose_name="Escola")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo de Movimentação")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade Movimentada")
    data = models.DateTimeField(default=timezone.now, verbose_name="Data da Movimentação")
    
    def __str__(self):
        return f"{self.get_tipo_display()} de {self.quantidade}x {self.item.nome}"