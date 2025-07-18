from django.urls import path

from .views import * # ou from . import views ai para cada view preciso colocar o prefixo views.

# app_name = "loja"

urlpatterns = [
    path('', homepage, name="homepage"), # Como configurar: ('caminho' ou link | a view que será carregada naquela página | nome interno: referenciar dentro do nosso site)
    path('loja/', loja, name="loja"), # Aula 6
    path('minhaconta/', minha_conta, name="minha_conta"), # Aula 6
    path('login/', login, name="login"), # Aula 6
    path('carrinho/', carrinho, name="carrinho"), # Aula 6
    path('checkout/', checkout, name="checkout"), # Aula 6
]
