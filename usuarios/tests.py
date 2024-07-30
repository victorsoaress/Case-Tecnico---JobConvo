from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import get_messages

class UserViewsTest(TestCase):
    
    def test_cadastro_get(self):
        """Verifica se a página de cadastro retorna um status code 200 no método GET"""
        response = self.client.get(reverse('cadastro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro.html')

    def test_cadastro_post_usuario_existente(self):
        """Verifica se a página de cadastro retorna um erro quando o usuário já existe"""
        User.objects.create_user(username='test@example.com', first_name='Test', password='password')
        response = self.client.post(reverse('cadastro'), {
            'email': 'test@example.com',
            'nome': 'Test',
            'senha': 'password',
            'tipo': 'Candidato'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após o erro
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Usuário já cadastrado no sistema.' for message in messages_list))

    def test_cadastro_post_sucesso(self):
        """Verifica se a página de cadastro cria um novo usuário com sucesso"""
        response = self.client.post(reverse('cadastro'), {
            'email': 'newuser@example.com',
            'nome': 'New User',
            'senha': 'SenhaSegura123!',
            'tipo': 'Candidato'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='newuser@example.com').exists())

    def test_cadastro_post_senha_invalida(self):
        """Verifica se a página de cadastro retorna um erro quando a senha não é válida"""
        response = self.client.post(reverse('cadastro'), {
            'email': 'newuser@example.com',
            'nome': 'New User',
            'senha': '123',  
            'tipo': 'Candidato'
        })
        self.assertEqual(response.status_code, 302)  
        response = self.client.get(reverse('cadastro'))  
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Esta senha é muito curta.' in str(message) for message in messages_list))
        self.assertTrue(any('Esta senha é inteiramente numérica.' in str(message) for message in messages_list))

    def test_login_get(self):
        """Verifica se a página de login retorna um status code 200 no método GET"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post_sucesso(self):
        """Verifica se o login é bem-sucedido com credenciais corretas"""
        User.objects.create_user(username='testuser@example.com', first_name='Test User', password='SenhaSegura123!')
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'senha': 'SenhaSegura123!'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_post_credenciais_invalidas(self):
        """Verifica se o login falha com credenciais incorretas"""
        User.objects.create_user(username='testuser@example.com', first_name='Test User', password='SenhaSegura123!')
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'senha': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 302)  # Verifica se redireciona após falha
        response = self.client.get(reverse('login'))  # Faz um novo GET para carregar as mensagens
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'E-mail ou senha inválidos.' for message in messages))
