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

    def __str__(self): # Usado para retornar o nome do objeto!! Por exemplo: Ao invés de voltar o Cliente.object(1), vai voltar o nome do cliente de fato. Ou o que vai "printar" para o usuário
        return str(self.nome)
# Categorias
class Categoria(models.Model): # (Masculino, Feminino, Infantil)
    nome = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return str(self.nome)

# Tipos
class Tipo(models.Model): # (Camisa, Camiseta, Calça)
    nome = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return str(self.nome)

# Produto
class Produto(models.Model):
    imagem = models.ImageField(null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL) # Relacionamento de tabelas, nesse caso Muitos para Um, e ao deletar uma categoria os campos vão ficar nulos
    tipo = models.ForeignKey(Tipo, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"Nome: {self.nome} - Categoria: {self.categoria} - Tipo: {self.tipo} - Preço: {self.preco}"
    

class Cor(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    codigo = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return str(self.nome)
    
    
# ItemEstoque
class ItemEstoque(models.Model):
    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.SET_NULL)
    cor = models.ForeignKey(Cor, null=True, blank=True, on_delete=models.SET_NULL)
    tamanho = models.CharField(max_length=200, null=True, blank=True)
    quantidade = models.IntegerField(default=0)
    
    def __str__(self):
        return str(f"{self.produto.nome}, Tamanho: {self.tamanho}, Cor: {self.cor.nome}")
    
    
# Endereco
class Endereco(models.Model):
    rua = models.CharField(max_length=400, null=True, blank=True)
    numero = models.IntegerField(default=0)
    complemento = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.complemento} - {self.cidade}-{self.estado} - {self.cep}'

# Pedido
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    finalizado = models.BooleanField(default=False)
    codigo_transacao = models.CharField(max_length=200, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
    data_finalizacao = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return str(f'Cliente: {self.cliente} | Id Pedido: {self.id} | Finalizado: {self.finalizado}')
    
    @property
    def quantidade_total(self):
        itens_pedido = ItensPedido.objects.filter(pedido__id=self.id)
        quantidade = sum(
            [item.quantidade for item in itens_pedido]
        )
        return quantidade
    
    @property
    def preco_total(self):
        itens_pedido = ItensPedido.objects.filter(pedido__id=self.id)
        preco = sum(
            [item.preco_total for item in itens_pedido]
        )
        return preco
    
# ItensPedido
class ItensPedido(models.Model):
    item_estoque = models.ForeignKey(ItemEstoque, null=True, blank=True, on_delete=models.SET_NULL)
    quantidade = models.IntegerField(default=0)
    pedido = models.ForeignKey(Pedido, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return str(f'Id Pedido: {self.pedido.id} | Produto: {self.item_estoque.produto.nome}, {self.item_estoque.tamanho}, {self.item_estoque.cor.nome}')
    
    @property # Estou dizendo que vou usar essa função sem precisar passar os parenteses, usando ela como se fosse um campo
    def preco_total(self): # posso criar métodos para a minha classe sem necessariamente criar um campo na tabela
        return self.quantidade * self.item_estoque.produto.preco


class Banner(models.Model):
    imagem = models.ImageField(null=True, blank=True)
    link_destino = models.CharField(max_length=400, null=True, blank=True)
    ativo = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{str(self.link_destino)} - Ativo: {self.ativo}"