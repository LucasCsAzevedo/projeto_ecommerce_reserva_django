from django.shortcuts import render
from .models import * # importando os nossos modelos para usar nas nossas views

'''
    Um site possui um frontend e um backend
    Frontend construído em HTML, CSS e JS
    Backend estamos usando Python com Django
'''

# Create your views here.
def homepage(request): # Toda função dentro da minha views precisa receber uma requisição, seja ela do tipo GET ou POST, Aula 5
    banners = Banner.objects.all()
    context = {"banners": banners}
    
    return render(request, 'homepage.html', context) # Por padrão a view precisa renderizar algo (render) através da requisição, uma homepage, Aula 5


def loja(request):
    produtos = Produto.objects.all() # Consulta na nossa tabela do banco para retornar todos os nossos produtos, famoso queryset
    context = {"produtos": produtos} # Variável que consigo acessar no meu template
    return render(request, 'loja.html', context)


def carrinho(request):
    return render(request, 'carrinho.html')


def checkout(request):
    return render(request, 'checkout.html')


def minha_conta(request): # template de autenticação do usuário
    return render(request, 'user/minha_conta.html')


def login(request): # template de autenticação do usuário
    return render(request, 'user/login.html')