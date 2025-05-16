from django.test import TestCase
from django.urls import reverse
from unifood_app.models import Usuario
from django.contrib.auth import get_user_model

User = get_user_model()

class UsuarioViewTest(TestCase):
    def test_usuario_view_get(self):
        """Teste de acesso à página de registro de usuário"""
        response = self.client.get(reverse('registrar'))  # ou 'usuarios:registrar' se tiver namespace
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'unifood_app/usuario/registrar.html')

        print("\nPágina de registro acessada com sucesso.")

    def test_verify_confirm_password(self):
        """Teste de verificação de senha"""

        # Dados que serão enviados no POST
        data = {
            'username': 'novo_usuario',
            'password': 'senha_forte',
            'confirm_password': 'senha_forte2',
            'email': 'email@test.com',
            'ra': '1234567890',
        }

        response = self.client.post('/registrar/', data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'As senhas devem ser iguais.')

        print("\nSenhas conferem.")

    def test_usuario_view_post(self):

        """Teste de criação de usuário via POST"""

        # Dados que serão enviados no POST
        data = {
            'username': 'novo_usuario',
            'password': 'senha_forte',
            'confirm_password': 'senha_forte',
            'email': 'email@test.com',
            'ra': '1234567890',
        }

        # Envia POST para a URL /registrar/
        response = self.client.post('/registrar/', data)

        # Verifica se o usuário foi criado
        user_exists = User.objects.filter(username='novo_usuario').exists()
        self.assertTrue(user_exists)

        # Verifica se o objeto Usuario foi criado com o RA correto
        usuario_exists = Usuario.objects.filter(ra='1234567890').exists()
        self.assertTrue(usuario_exists)

        # Verifica se a resposta é um redirecionamento (status 302)
        self.assertEqual(response.status_code, 302)
        print("\nUsuário criado com sucesso.")

    def test_ra_already_exists(self):
        """Teste de verificação de RA já existente"""

        user1 = {
            'username': 'novo_usuario',
            'password': 'senha_forte',
            'confirm_password': 'senha_forte',
            'email': 'email@test.com',
            'ra': '1234567890',
        }

        user2 = {
            'username': 'outro_usuario',
            'password': 'senha_forte',
            'confirm_password': 'senha_forte',
            'email': 'email@test.com',
            'ra': '1234567890',
        }

        # Cria o primeiro usuário
        self.client.post('/registrar/', user1)
        # Tenta criar o segundo usuário com o mesmo RA
        response = self.client.post('/registrar/', user2)
        # Verifica se a mensagem de erro está presente na resposta 
        self.assertContains(response, 'RA já cadastrado.')
        print("\nRA já cadastrado.")
    
    def test_username_already_exists(self):
        """Teste de verificação de username já existente"""

        user1 = {
            'username': 'novo_usuario',
            'password': 'senha_forte',
            'confirm_password': 'senha_forte',
            'email': 'email@test.com',
            'ra': '123456432',
        }

        user2 = {
            'username': 'novo_usuario',
            'password': 'senha_forte',
            'confirm_password': 'senha_forte',
            'email': 'email@test.com',
            'ra': '1234567890',
        }

        self.client.post('/registrar/', user1)
        response = self.client.post('/registrar/', user2)

        # Verifica se a mensagem de erro está presente na resposta
        self.assertContains(response, 'Usuário já cadastrado.')

    print("\nUsuario já cadastrado.")

    def test_email_already_exists(self):
        """Teste de verificação de email já existente"""

        user1 = {
            'username': 'novo_usuario',
            'password': 'senha_forte',
            'confirm_password': 'senha_forte',
            'email': 'teste@gmail.com',
            'ra': '1234567890',
        }
        user2 = {
            'username': 'outro_usuario',
            'password': 'senha_forte',
            'confirm_password': 'senha_forte',
            'email': 'teste@gmail.com',
            'ra': '1234567891',
        }    

        self.client.post('/registrar/', user1)
        response = self.client.post('/registrar/', user2)
        # Verifica se a mensagem de erro está presente na resposta  
        self.assertContains(response, 'Email já cadastrado.')
        
        print("\nEmail já cadastrado.")               