from django.shortcuts import redirect, render
from .models import * # importando os nossos modelos para usar nas nossas views
import uuid # Gerar números aleatórios não repetidos, usados para nosso id_sessao

'''
    Um site possui um frontend e um backend
    Frontend construído em HTML, CSS e JS
    Backend estamos usando Python com Django
'''

# Create your views here.
def homepage(request): # Toda função dentro da minha views precisa receber uma requisição, seja ela do tipo GET ou POST, Aula 5
    banners = Banner.objects.filter(ativo=True) # Filtrando o objeto conforme os parâmetros que ele tem
    context = {"banners": banners}
    
    return render(request, 'homepage.html', context) # Por padrão a view precisa renderizar algo (render) através da requisição, uma homepage, Aula 5


def loja(request, nome_categoria=None): # acrescentei o valor dinâmico "nome_categoria"
    produtos = Produto.objects.filter(ativo=True) # Consulta na nossa tabela do banco para retornar todos os nossos produtos, famoso queryset
    if nome_categoria:
        produtos = produtos.filter(categoria__nome=nome_categoria) # Filtrando de forma mais performática
    context = {"produtos": produtos} # Variável que consigo acessar no meu template
    return render(request, 'loja.html', context)


def ver_produto(request, id_produto, id_cor=None):
    tem_estoque = False
    cores = {}
    tamanhos = {}
    cor_selecionada = None
    if id_cor:
        cor_selecionada = Cor.objects.get(id=id_cor)
    produto = Produto.objects.get(id=id_produto)
    itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0) # Esse filtro de quantidade é equivalente a quantidade > 0 (pesquisar por django querysets)
    if len(itens_estoque) > 0:
        tem_estoque = True
        cores = {item.cor for item in itens_estoque} # Para aparecer somente os valores distintos preciso passar um set, dentro de um colchetes
        if id_cor:
            itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0, cor__id=id_cor)
            tamanhos = {item.tamanho for item in itens_estoque}
            
    context = {
        "produto": produto,
        "tem_estoque": tem_estoque,
        "cores": cores,
        "tamanhos": tamanhos,
        "cor_selecionada": cor_selecionada
    }
    return render(request, "ver_produto.html", context)


def adicionar_carrinho(request, id_produto):
    if request.method == 'POST' and id_produto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        id_cor = dados.get("cor")
        if not tamanho:
            return redirect('loja')
               
        resposta = redirect('carrinho')
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else: # Criar o cliente anônimo, criar um id_sessao e armazenar no cookie do navegador
            if request.COOKIES.get('id_sessao'):
                id_sessao = request.COOKIES.get('id_sessao')
            else:
                id_sessao = str(uuid.uuid4()) # Por que o uuid4? Porque ele gera o randômico sem que os números se repitam
                resposta.set_cookie(key="id_sessao", value=id_sessao, max_age=2592000) # Adicionando um tempo máximo que o cookie dura no navegador do usuário, está em segundos
                
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao) # get_or_create sempre retorna duas informações, criado é sempre "padrão"
            
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False) # TODO Revisar! Aula 34
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, tamanho=tamanho, cor__id=id_cor) # TODO Revisar! Aula 34
        item_pedido, criado = ItensPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido) # TODO Revisar! Aula 34
        item_pedido.quantidade += 1 # TODO Revisar! Aula 34
        item_pedido.save() # TODO Revisar! Aula 34
        
        return resposta
    else:
        return redirect('loja') # Redirecionando para nossa loja, através do nome que definimos na url
    
    
def remover_carrinho(request, id_produto):
    if request.method == 'POST' and id_produto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        id_cor = dados.get("cor")
        if not tamanho:
            return redirect('loja')
        
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get("id_sessao"):
                id_sessao = request.COOKIES.get("id_sessao")
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                return redirect('loja')
            
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False) # TODO Revisar! Aula 34
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, tamanho=tamanho, cor__id=id_cor) # TODO Revisar! Aula 34
        item_pedido, criado = ItensPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido) # TODO Revisar! Aula 34
        item_pedido.quantidade -= 1
        item_pedido.save()
        if item_pedido.quantidade <= 0:
            item_pedido.delete()
        
        return redirect('carrinho')


def carrinho(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("id_sessao"):
            id_sessao = request.COOKIES.get('id_sessao')
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            context = {
                "cliente_existente": False,
                 "pedido": None,
                "itens_pedido": None
            }
            return render(request, 'carrinho.html', context)
        
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False) # O django já tem essa função para caso não encontrar o pedido, criar ele.
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)      
    context = {
        "pedido": pedido,
        "itens_pedido": itens_pedido,
        "cliente_existente": True
    }
    return render(request, 'carrinho.html', context)
    

def checkout(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("id_sessao"):
            id_sessao = request.COOKIES.get('id_sessao')
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            return redirect('loja')
        
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False) # O django já tem essa função para caso não encontrar o pedido, criar ele.
    enderecos = Endereco.objects.filter(cliente=cliente)
    context = {
        "pedido": pedido,
        "enderecos": enderecos,
    }
    return render(request, 'checkout.html', context)


def adicionar_endereco(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get("id_sessao"):
                id_sessao = request.COOKIES.get('id_sessao')
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                return redirect('loja')
        dados = request.POST.dict()
        endereco = Endereco.objects.create(
            cliente=cliente,
            rua=dados.get('rua'),
            numero=int(dados.get('numero')),
            complemento=dados.get('complemento'),
            cep=dados.get('cep'),
            cidade=dados.get('cidade'),
            estado=dados.get('estado'),
        )
        endereco.save() # Como estou criando um dado no banco, talvez não tenha necessidade de salvar
        return redirect('checkout')
    else:
        context = {}
        return render(request, 'adicionar_endereco.html', context)


def minha_conta(request): # template de autenticação do usuário
    return render(request, 'user/minha_conta.html')


def login(request): # template de autenticação do usuário
    return render(request, 'user/login.html')

# TODO sempre que o usuario criar uma conta no nosso site vamos precisar criar um cliente para ele, fazer uma função