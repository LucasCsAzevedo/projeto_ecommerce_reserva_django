from django.shortcuts import render
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


def ver_produto(request, id_produto):
    produto = Produto.objects.get(id=id_produto)
    context = {"produto":produto}
    return render(request, "ver_produto.html", context)


def carrinho(request):
    return render(request, 'carrinho.html')


def checkout(request):
    return render(request, 'checkout.html')


def minha_conta(request): # template de autenticação do usuário
    return render(request, 'user/minha_conta.html')


def login(request): # template de autenticação do usuário
    return render(request, 'user/login.html')