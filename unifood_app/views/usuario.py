from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages
from unifood_app.models import Usuario
from unifood_app.forms import RegisterForm, LoginForm


# Create your views here.
def Login(requests):

    if requests.method == 'POST':
        form = LoginForm(requests.POST)

        if form.is_valid():
            ra = form.cleaned_data['ra']
            password = form.cleaned_data['password']

            try:
                user = Usuario.objects.get(ra=ra)
                user = authenticate(requests, username=user.user.username, password=password)

                if user:
                    login(requests, user)
                    messages.success(requests, 'Login realizado com sucesso!')
            except:
                messages.error(requests,f'Invalid RA or password')
                return render(requests,'unifood_app/usuario/login.html',{'form': form})

    elif requests.method == 'GET':
        form = LoginForm()
        return render(requests, 'unifood_app/usuario/login.html', {'form':form})

def Registrar(requests):
    if requests.method == 'POST':
        form = RegisterForm(requests.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            ra = form.cleaned_data['ra']

            if password != confirm_password:
                
                return render(requests, 'unifood_app/usuario/registrar.html', {
                    'form': form,
                    'error': 'As senhas devem ser iguais.'
                })
            if Usuario.objects.filter(ra=ra).exists():
                return render(requests, 'unifood_app/usuario/registrar.html', {
                    'form': form,
                    'error': 'RA já cadastrado.'
                })
            if Usuario.objects.filter(user__username=username).exists():
                return render(requests, 'unifood_app/usuario/registrar.html', {
                    'form': form,
                    'error': 'Usuário já cadastrado.'
                })
            
            if Usuario.objects.filter(user__email=email).exists():
                return render(requests, 'unifood_app/usuario/registrar.html', {
                    'form': form,
                    'error': 'Email já cadastrado.'
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
        form = RegisterForm()
        return render(requests, 'unifood_app/usuario/registrar.html', {'form': form})