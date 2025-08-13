

def filtrar_produtos(produtos, filtro):
    if filtro:
        if '-' in filtro:
            categoria, tipo = filtro.split('-') # Famoso unpacking!
            produtos = produtos.filter(categoria__slug=categoria, tipo__slug=tipo)
        else:
            produtos = produtos.filter(categoria__slug=filtro) # Filtrando de forma mais performática
            
    return produtos