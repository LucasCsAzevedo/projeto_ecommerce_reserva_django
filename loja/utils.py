from django.db.models import Min, Max # Importando filtros de agregação


def filtrar_produtos(produtos, filtro):
    if filtro:
        if '-' in filtro:
            categoria, tipo = filtro.split('-') # Famoso unpacking!
            produtos = produtos.filter(categoria__slug=categoria, tipo__slug=tipo)
        else:
            produtos = produtos.filter(categoria__slug=filtro) # Filtrando de forma mais performática
            
    return produtos


def preco_minimo_maximo(produtos):
    minimo, maximo = (0, 0)
    if len(produtos) > 0:
        minimo = round(list(produtos.aggregate(Min('preco')).values())[0], 2) # Transformando em uma lista (porque retorna um dict values) para conseguir pegar o primeiro valor
        maximo = round(list(produtos.aggregate(Max('preco')).values())[0], 2) # Como ele retorna um objeto (aggregate) preciso colocar um .values() para me mostrar os valores
        
    return minimo, maximo