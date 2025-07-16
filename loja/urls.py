from django.urls import path

from .views import * # ou from . import views ai para cada view preciso colocar o prefixo views.

app_name = "loja"

urlpatterns = [
    path('', homepage, name="homepage") # Como configurar: ('caminho' ou link | a view que será carregada naquela página | nome interno: referenciar dentro do nosso site)
]
