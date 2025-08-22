from django.urls import path
from django.contrib.auth import views
from .views import * # ou from . import views ai para cada view preciso colocar o prefixo views.

# app_name = "loja"

urlpatterns = [
    path('', homepage, name="homepage"), # Como configurar: ('caminho' ou link | a view que será carregada naquela página | nome interno: referenciar dentro do nosso site)
    path('loja/', loja, name="loja"), # Aula 6
    path('loja/<str:filtro>/', loja, name="loja"), # Criando um link dinâmico, geralmente não colocamos valores dinâmicos como o primeiro parâmetro da url
    path('produto/<int:id_produto>/', ver_produto, name="ver_produto"),
    path('produto/<int:id_produto>/<int:id_cor>/', ver_produto, name="ver_produto"),
    path('carrinho/', carrinho, name="carrinho"), # Aula 6
    path('checkout/', checkout, name="checkout"), # Aula 6
    path('adicionarcarrinho/<int:id_produto>/', adicionar_carrinho, name="adicionar_carrinho"),
    path('removercarrinho/<int:id_produto>/', remover_carrinho, name="remover_carrinho"),
    path('adicionarendereco/', adicionar_endereco, name="adicionar_endereco"),
    path('minhaconta/', minha_conta, name="minha_conta"), # Aula 6
    path('fazerlogin/', fazer_login, name="fazer_login"), # Aula 6
    path('fazerlogout/', fazer_logout, name="fazer_logout"), # Aula 6
    path('criarconta/', criar_conta, name="criar_conta"), # Aula 6
    
    path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
