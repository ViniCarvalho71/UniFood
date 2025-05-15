from django.test import TestCase
from django.contrib.auth import get_user_model
from unifood_app.models import Usuario

class UsuarioModelTest(TestCase):
    def setUp(self):
        # Configura um usuário para usar nos testes
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_usuario_creation(self):
        # Testa a criação de um objeto Usuario com um usuário válido
        usuario = Usuario.objects.create(user=self.user)
        self.assertEqual(usuario.user, self.user, msg="Falha: O usuário associado ao objeto Usuario não corresponde ao esperado.")
        self.assertEqual(usuario.user.username, 'testuser', msg="Falha: O nome de usuário não foi salvo corretamente.")
        self.assertEqual(usuario.user.email, 'test@example.com', msg="Falha: O email do usuário não foi salvo corretamente.")

        print("Sucesso: O objeto Usuario foi criado corretamente com o usuário esperado.")