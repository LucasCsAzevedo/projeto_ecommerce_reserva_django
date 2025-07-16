from django.shortcuts import render

'''
    Um site possui um frontend e um backend
    Frontend construído em HTML, CSS e JS
    Backend estamos usando Python com Django
'''

# Create your views here.
def homepage(request): # Toda função dentro da minha views precisa receber uma requisição, seja ela do tipo GET ou POST, Aula 5
    return render(request, 'homepage.html') # Por padrão a view precisa renderizar algo (render) através da requisição, uma homepage, Aula 5