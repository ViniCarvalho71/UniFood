from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from unifood_app.models import Produto
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

User = get_user_model()

class ProdutoViewTest(TestCase):
    def setUp(self):
        """ Cria um usuário e um produto para os testes """
        
        # Criando um usuário
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpassword'
        )

        # Logando o usuário
        self.client.login(username='testuser', password='testpassword')

        # Criando um produto
        self.produto_imagem = SimpleUploadedFile(
            name='produto.jpg',
            content=b'produto_image_content',
            content_type='image/jpeg'
        )

        self.produto = Produto.objects.create(
            nome='Produto Teste',
            descricao='Descrição do produto de teste',
            preco=100.00,
            estoque=50,
            vendedor=self.user,
            foto=self.produto_imagem
        )

    def test_produto_cadastro_view(self):
        """ Teste de visualização de cadastro de produto """
        
        response = self.client.get(reverse('cadastro'))
        
        # Verifica se a página de cadastro é renderizada corretamente
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cadastro Produto')



    def test_feed_produtos_view(self):
        """ Teste de visualização do feed de produtos """
        
        response = self.client.get(reverse('feed'))

        # Verifica se o feed foi renderizado corretamente
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Produto Teste')


    def test_produto_create_api(self):
        """ Teste de criação de produto via API """
        
        data = {
            'nome': 'Produto API',
            'descricao': 'Produto de teste via API',
            'preco': 200.00,
            'estoque': 40,
        }

        # Criando o produto via API
        response = self.client.post(reverse('cadastro'), data)

        # Verificando se o produto foi criado
        self.assertEqual(response.status_code, 302)
        produto_api = Produto.objects.get(nome='Produto API')
        self.assertEqual(produto_api.preco, 200.00)

    def test_produto_create_api_sem_authentication(self):
        """ Teste de criação de produto via API sem autenticação """
        
        # Criando o produto via API sem autenticação
        data = {
            'nome': 'Produto API Sem Auth',
            'descricao': 'Produto sem autenticação',
            'preco': 250.00,
            'estoque': 50,
        }

        response = self.client.post(reverse('api-produto-create'), data)

        # Verificando se a API retorna erro de autenticação
        self.assertEqual(response.status_code, 400)
