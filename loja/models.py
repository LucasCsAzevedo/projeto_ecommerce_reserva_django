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


# Produto
    # imagem
    # nome
    # preco
    # ativo
    # categoria
    # tipo
    
# Categorias
    # nome

# Tipos
    # nome
    
# ItemEstoque
    # produto
    # cor
    # tamanho
    # quantidade
    
    
# ItensPedido
    # itemestoque
    # quantidade
    
# Pedido
    # cliente
    # data_finalizacao
    # finalizado
    # id_transacao
    # endereco
    # itenspedido
    
# Endereco
    # rua
    # numero
    # complemento
    # cep
    # cidade
    # estado
    # cliente