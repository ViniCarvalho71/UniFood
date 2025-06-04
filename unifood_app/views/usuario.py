from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from unifood_app.models import Usuario
from unifood_app.forms import RegisterForm, LoginForm


# Create your views here.
def Login(requests):
    if requests.user.is_authenticated:
            return redirect('/produto/feed_produtos', {
                        'is_authenticated': True,
                    }) 

    if requests.method == 'POST':
        form = LoginForm(requests.POST)

        # Validando formulário
        if form.is_valid():
            ra = form.cleaned_data['ra']
            password = form.cleaned_data['password']

            try:
                user = Usuario.objects.get(ra=ra)
                user = authenticate(requests, username=user.user.username, password=password)

                if user is not None:
                    login(requests, user)
                    return redirect('/produto/feed_produtos', {
                        'user': user,
                        'success': 'Login realizado com sucesso!',
                    })
                else:
                    messages.error(requests,f'Credenciais inválidas!')
                    return render(requests,'unifood_app/usuario/login.html',{
                            'form': form,
                            'error': 'Credenciais inválidas!'
                        })
            except:
                messages.error(requests,f'Credenciais inválidas!')
                return render(requests,'unifood_app/usuario/login.html',{
                        'form': form,
                        'error': 'Credenciais inválidas!'
                    })

    elif requests.method == 'GET':
        form = LoginForm()
        return render(requests, 'unifood_app/usuario/login.html', {'form':form})


    elif requests.method == 'GET':
        form = RegisterForm()
        return render(requests, 'unifood_app/usuario/registrar.html', {'form': form})
    
def Logout(requests):
    logout(requests)
    form = LoginForm()
    return redirect('/login/', {form: form})