from django.shortcuts import render, HttpResponse

# Create your views here.
def Login(requests):
    return render(requests, 'unifood_app/usuario/login.html')