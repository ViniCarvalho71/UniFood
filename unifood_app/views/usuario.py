from django.shortcuts import render, HttpResponse

# Create your views here.
def homeView(requests):
    return HttpResponse("Hello World!")