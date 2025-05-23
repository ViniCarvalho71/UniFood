from django.shortcuts import render, HttpResponse, redirect
from unifood_app.forms import ProdutoForm

def Cadastro(request):
    form = ProdutoForm()
    return render(request, "unifood_app/produto/cadastro.html", {'form': form})
