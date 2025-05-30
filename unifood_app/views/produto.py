from django.shortcuts import render, redirect
from unifood_app.forms import ProdutoForm

def Cadastro(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)

            # Verifica se o usuário está autenticado antes de associar
            if request.user.is_authenticated:
                produto.vendedor = request.user

            produto.save()
            return redirect('cadastro')  # ou qualquer outra URL válida
    else:
        form = ProdutoForm()

    return render(request, "unifood_app/produto/cadastro.html", {'form': form})

def feed_produtos(request):
    produtos = ProdutoForm()
    return render(request, 'unifood_app/produto/Feed.html', {'produtos': produtos})
