from rest_framework import generics, permissions
from unifood_app.models import Produto
from ..serializers import ProdutoSerializer

class ProdutoCreateAPIView(generics.CreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(vendedor=self.request.user)
