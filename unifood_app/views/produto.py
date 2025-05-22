from django.shortcuts import render, HttpResponse, redirect


def Cadastro(request):
    return render(request, "unifood_app/produto/cadastro.html")
