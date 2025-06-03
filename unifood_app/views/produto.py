from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from unifood_app.models import Produto
from unifood_app.serializers import ProdutoSerializer
from unifood_app.forms import ProdutoForm

# View tradicional para cadastro via formulário HTML
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
def feed_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'unifood_app/produto/Feed.html', {'produtos': produtos})

# API REST para cadastro de produto
class ProdutoCreateAPIView(generics.CreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    #permission_classes = [permissions.IsAuthenticated]  # só usuário autenticado pode criar

    def perform_create(self, serializer):
        serializer.save(vendedor=self.request.user)  # associa vendedor automaticamente
