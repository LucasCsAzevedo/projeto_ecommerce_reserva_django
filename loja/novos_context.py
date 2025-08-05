# Vou colocar as funções que precisam aparecer em todas as páginas
from .models import *

def carrinho(request):
    quantidade_produtos_carrinho = 0
    
    if request.user.is_authenticated:
        cliente = request.user.cliente # Consigo pegar o cliente através do user, como existe um relacionamento OnetoOne eu poderia fazer isso inverso: cliente.user
    else:
        return {"quantidade_produtos_carrinho": quantidade_produtos_carrinho}
        
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False) # O django já tem essa função para caso não encontrar o pedido, criar ele.
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    
    for item in itens_pedido:
        quantidade_produtos_carrinho += item.quantidade

    return {"quantidade_produtos_carrinho": quantidade_produtos_carrinho}