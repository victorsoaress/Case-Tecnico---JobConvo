from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.db.utils import IntegrityError
from .models import Vaga

class VagaViewsTest(TestCase):
    def setUp(self):
        # Cria um usuário de teste e o adiciona ao grupo 'empresa'
        self.empresa_group = Group.objects.create(name='empresa', id='2')
        self.user = User.objects.create_user(username='empresa@example.com', password='senha')
        self.empresa_group.user_set.add(self.user)
        self.client.login(username='empresa@example.com', password='senha')

        # URLs para teste
        self.criar_vagas_url = reverse('criar_vagas')
        self.listar_vagas_adm_url = reverse('listar_vagas_adm')
        self.editar_vaga_url = lambda id: reverse('editar_vaga', args=[id])
        self.deletar_vaga_url = lambda id: reverse('deletar_vaga', args=[id])

        # Cria uma vaga de teste
        self.vaga = Vaga.objects.create(
            nome='Vaga de Teste',
            requisitos='Requisitos da vaga.',
            faixa_salarial='2000-3000',
            escolaridade_minima='superior'
        )

    def test_criar_vaga_sucesso(self):
        """Verifica se o processo de criação de vaga está funcionando corretamente"""
        response = self.client.post(self.criar_vagas_url, {
            'nome': 'Nova Vaga',
            'requisitos': 'Requisitos da nova vaga.',
            'faixa_salarial': '3000-100000',
            'escolaridade_minima': 'superior'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após salvar a vaga
        self.assertTrue(Vaga.objects.filter(nome='Nova Vaga').exists())

    def test_criar_vaga_sem_dados(self):
        """Verifica se a criação de vaga sem dados não funciona"""
        response = self.client.post(self.criar_vagas_url, {})
        self.assertEqual(response.status_code, 200)  # Retorna ao formulário com erros

    def test_listar_vagas_adm(self):
        """Verifica se a listagem de vagas está funcionando corretamente"""
        response = self.client.get(self.listar_vagas_adm_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vaga de Teste')

    def test_editar_vaga(self):
        """Verifica se a edição de vaga está funcionando corretamente"""
        response = self.client.post(self.editar_vaga_url(self.vaga.id), {
            'nome': 'Vaga Editada',
            'requisitos': 'Requisitos atualizados.',
            'faixa_salarial': '1000-2000',
            'escolaridade_minima': 'medio'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após salvar a edição
        self.vaga.refresh_from_db()
        self.assertEqual(self.vaga.nome, 'Vaga Editada')

    def test_deletar_vaga(self):
        """Verifica se a exclusão de vaga está funcionando corretamente"""
        response = self.client.post(self.deletar_vaga_url(self.vaga.id))
        self.assertEqual(response.status_code, 302)  # Redireciona após deletar
        with self.assertRaises(Vaga.DoesNotExist):
            Vaga.objects.get(id=self.vaga.id)
