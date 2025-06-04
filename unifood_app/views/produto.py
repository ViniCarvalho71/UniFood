from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from unifood_app.models import Produto, Usuario
from unifood_app.serializers import ProdutoSerializer
from unifood_app.forms import ProdutoForm
from django.contrib.auth.decorators import login_required

# View tradicional para cadastro via formulário HTML
@login_required
def Cadastro(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            if request.user.is_authenticated:
                produto.vendedor = request.user
            produto.save()
            return redirect('cadastro')  # pode mudar para outra rota se quiser
    else:
        form = ProdutoForm()
    return render(request, "unifood_app/produto/cadastro.html", {'form': form})

# View tradicional para mostrar lista de produtos no template
@login_required
def feed_produtos(request):
    produtos = Produto.objects.all()
    eh_vendedor = Usuario.objects.filter(user=request.user, eh_vendedor=1).exists()  # Verifica se o usuário é vendedor

    return render(request, 'unifood_app/produto/Feed.html', {'produtos': produtos, 'eh_vendedor': eh_vendedor})

# API REST para cadastro de produto
class ProdutoCreateAPIView(generics.CreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    #permission_classes = [permissions.IsAuthenticated]  # só usuário autenticado pode criar

    def perform_create(self, serializer):
        serializer.save(vendedor=self.request.user)  # associa vendedor automaticamente
