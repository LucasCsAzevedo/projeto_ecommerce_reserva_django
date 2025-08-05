from django.shortcuts import redirect, render
from .models import * # importando os nossos modelos para usar nas nossas views

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
        print(dados)
        tamanho = dados.get("tamanho")
        id_cor = dados.get("cor")
        if not tamanho:
            return redirect('loja')
        return redirect('carrinho')
    else:
        return redirect('loja') # Redirecionando para nossa loja, através do nome que definimos na url


def carrinho(request):
    return render(request, 'carrinho.html')


def checkout(request):
    return render(request, 'checkout.html')


def minha_conta(request): # template de autenticação do usuário
    return render(request, 'user/minha_conta.html')


def login(request): # template de autenticação do usuário
    return render(request, 'user/login.html')

# TODO sempre que o usuario criar uma conta no nosso site vamos precisar criar um cliente para ele, fazer uma função