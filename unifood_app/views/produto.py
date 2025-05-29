from django.shortcuts import render, HttpResponse, redirect
from unifood_app.forms import ProdutoForm

def Cadastro(request):
    form = ProdutoForm()
    return render(request, "unifood_app/produto/cadastro.html", {'form': form})

def feed_produtos(request):
    produtos = ProdutoForm()
    return render(request, 'unifood_app/produto/Feed.html', {'produtos': produtos})
