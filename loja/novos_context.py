# Vou colocar as funções que precisam aparecer em todas as páginas
from .models import *

def carrinho(request):
    quantidade_produtos_carrinho = 4 # Valor inicial
    return {"quantidade_produtos_carrinho": quantidade_produtos_carrinho}