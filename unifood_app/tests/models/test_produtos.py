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

    def test_produto_create_view(self):
        """ Teste de criação de produto através do formulário """
        
        data = {
            'nome': 'Produto Novo',
            'descricao': 'Produto de teste novo',
            'preco': 150.00,
            'estoque': 30,
            'foto': self.produto_imagem
        }

        response = self.client.post(reverse('cadastro'), data)

        # Verificando se o produto foi criado corretamente
        produto_novo = Produto.objects.get(nome='Produto Novo')
        self.assertEqual(produto_novo.nome, 'Produto Novo')
        self.assertEqual(produto_novo.preco, 150.00)

        # Verificando o redirecionamento após a criação
        self.assertRedirects(response, reverse('feed'))

    def test_feed_produtos_view(self):
        """ Teste de visualização do feed de produtos """
        
        response = self.client.get(reverse('feed'))

        # Verifica se o feed foi renderizado corretamente
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Produto Teste')

    def test_feed_produtos_verifica_vendedor(self):
        """ Teste para verificar a variável 'eh_vendedor' """
        
        response = self.client.get(reverse('feed'))

        # Verificando se a variável 'eh_vendedor' está no contexto
        self.assertIn('eh_vendedor', response.context)
        self.assertTrue(response.context['eh_vendedor'], msg="O usuário não é identificado como vendedor")

    def test_produto_create_api(self):
        """ Teste de criação de produto via API """
        
        data = {
            'nome': 'Produto API',
            'descricao': 'Produto de teste via API',
            'preco': 200.00,
            'estoque': 40,
        }

        # Criando o produto via API
        response = self.client.post(reverse('api-produto-create'), data)

        # Verificando se o produto foi criado
        self.assertEqual(response.status_code, 201)
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
        self.assertEqual(response.status_code, 401)

    # Teste de exclusão de produto (se houver na view)
    def test_produto_delete(self):
        """ Teste de exclusão de produto """
        
        produto = Produto.objects.create(
            nome='Produto a Ser Excluído',
            descricao='Produto de teste a ser excluído',
            preco=50.00,
            estoque=10,
            vendedor=self.user
        )
        
        # Verificando a contagem antes da exclusão
        self.assertEqual(Produto.objects.count(), 2)
        
        # Acessando a view de exclusão
        response = self.client.post(reverse('produto_deletar', args=[produto.id]))
        
        # Verificando a exclusão
        self.assertEqual(Produto.objects.count(), 1)
        self.assertRedirects(response, reverse('feed'))
