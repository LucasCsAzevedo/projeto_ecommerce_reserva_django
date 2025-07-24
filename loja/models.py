from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# As nossas tabelas são classes do Python
# O campo id é criado automaticamente pelo django

class Cliente(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True) # tipo do nosso campo e os seus parâmetros, campo com tamanho de 200 caracteres, pode ser nulo e em branco
    email = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=200, null=True, blank=True)
    id_sessao = models.CharField(max_length=200, null=True, blank=True)
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) # Relacionamento de tabelas, nesse caso Um para Um com a tabela de Users nativa do django, como parâmetro vou passar a tabela que está sendo relacionada, e no caso de campos com relacionamento preciso passar o on_delete, caso deletar o usuário o que vai acontecer?

# Categorias
class Categoria(models.Model): # (Masculino, Feminino, Infantil)
    nome = models.CharField(max_length=200, null=True, blank=True)

# Tipos
class Tipo(models.Model): # (Camisa, Camiseta, Calça)
    nome = models.CharField(max_length=200, null=True, blank=True)

# Produto
class Produto(models.Model):
    imagem = models.CharField(max_length=400, null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL) # Relacionamento de tabelas, nesse caso Muitos para Um, e ao deletar uma categoria os campos vão ficar nulos
    tipo = models.ForeignKey(Tipo, null=True, blank=True, on_delete=models.SET_NULL)
    
# ItemEstoque
class ItemEstoque(models.Model):
    produto = models.ForeignKey(Tipo, null=True, blank=True, on_delete=models.SET_NULL)
    cor = models.CharField(max_length=200, null=True, blank=True)
    tamanho = models.CharField(max_length=200, null=True, blank=True)
    quantidade = models.IntegerField(default=0)
    
# Endereco
class Endereco(models.Model):
    rua = models.CharField(max_length=400, null=True, blank=True)
    numero = models.IntegerField(default=0)
    complemento = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)

# Pedido
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    finalizado = models.BooleanField(default=False)
    codigo_transacao = models.CharField(max_length=200, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
    data_finalizacao = models.DateTimeField(null=True, blank=True)
    
# ItensPedido
class ItensPedido(models.Model):
    item_estoque = models.ForeignKey(ItemEstoque, null=True, blank=True, on_delete=models.SET_NULL)
    quantidade = models.IntegerField(default=0)
    pedido = models.ForeignKey(Pedido, null=True, blank=True, on_delete=models.SET_NULL)
