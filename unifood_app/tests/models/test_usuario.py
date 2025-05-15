from django.test import TestCase
from django.contrib.auth import get_user_model
from unifood_app.models import Usuario
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UsuarioModelTest(TestCase):
    def setUp(self):
        """ Cria um usuário de teste """
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='teste@email.com',
            password='password',
        )

        # Criando usuário do modelo Usuario
        self.usuario = Usuario.objects.create(
            user=self.user,
            ra='2002222',
        )

    def test_usuario_creation(self):
        """ Teste de Criação de Usuário """

        # Quando queremos buscar um valor de uma chave estrangeira, usamos o '__' para separar os campos
        usuario_teste = Usuario.objects.get(user__username='testuser')

        # Como o modelo Usuário só tem o campo "user" e "ra",
        # para pegar os campos dentro do modelo "user", precisamos usar o '__'
        # já o campo "ra" é direto

        self.assertEqual(usuario_teste.user.username, 'testuser', msg="Usuário não encontrado")
        self.assertEqual(usuario_teste.user.email, 'teste@email.com', msg="Email não encontrado")

        # Como a senha é criptografada, não podemos verificar diretamente, tem que usar essa função de check_password()
        self.assertTrue(usuario_teste.user.check_password('password'), msg="Senha incorreta")
        self.assertEqual(usuario_teste.ra, '2002222', msg="RA não encontrado")

        print("\nUsuário Cadastrado com Sucesso!")

    def test_usuario_authentication(self):
        """ Teste de Autenticação de Usuário """
        
        usuario_auth = authenticate(username='testuser', password='password')
        self.assertIsNotNone(usuario_auth, msg="Usuário não autenticado")

        print("\nUsuário Autenticado com Sucesso!")

    def test_usuario_email_validation(self):
        """ Teste de Validação de Email """
        
        usuario_teste = Usuario.objects.get(user__username='testuser')
        email = usuario_teste.user.email

        try:
            validate_email(email)
        except ValidationError:
            self.fail("Email inválido")
        
        print("\nEmail Válido!")
