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

    def test_usuario_view_post(self):

        """Teste de criação de usuário via POST"""

        # Dados que serão enviados no POST
        data = {
            'username': 'novo_usuario',
            'password': 'senha_forte',
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
