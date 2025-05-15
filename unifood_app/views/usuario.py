from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model
from unifood_app.models import Usuario


# Create your views here.
def Login(requests):
    return render(requests, 'unifood_app/usuario/login.html')

def Registrar(requests):
    if requests.method == 'POST':
        username = requests.POST.get('username')
        email = requests.POST.get('email')
        password = requests.POST.get('password')
        confirm_password = requests.POST.get('confirm_password')
        ra = requests.POST.get('ra')

        if password != confirm_password:
            return render(requests, 'unifood_app/usuario/registrar.html', {
                'erro': 'As senhas devem ser iguais.'
            })
        
        User = get_user_model()
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        Usuario.objects.create( 
            user=user,
            ra=ra,
        )
        

        return redirect('/login/')
    elif requests.method == 'GET':
        return render(requests, 'unifood_app/usuario/registrar.html')