# candidaturas/tests.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from vagas.models import Vaga
from .models import Candidatura
from django.urls import reverse
from django.utils import timezone
from django.contrib.messages import get_messages


class CandidaturaModelTest(TestCase):
    def setUp(self):
        """Cria usuários, vagas e candidaturas para os testes"""
        self.usuario = User.objects.create_user(username='candidato', password='senha')
        self.empresa = User.objects.create_user(username='empresa', password='senha')
        self.vaga = Vaga.objects.create(
            nome="Desenvolvedor Django",
            requisitos="Conhecimento avançado em Django e Python.",
            faixa_salarial="2000-3000",
            escolaridade_minima="superior"
        )
        self.candidatura = Candidatura.objects.create(
            candidato=self.usuario,
            vaga=self.vaga,
            pretensao_salarial=2500.00,
            experiencia="3 anos de experiência em Django.",
            escolaridade="superior"
        )

    def test_candidatura_str(self):
        """Verifica se o método '__str__' retorna o formato esperado"""
        self.assertEqual(str(self.candidatura), "candidato - Desenvolvedor Django")

    def test_calcular_pontuacao(self):
        """Verifica se a pontuação é calculada corretamente"""
        pontuacao = self.candidatura.calcular_pontuacao()
        self.assertEqual(pontuacao, 2)  # Deve adicionar 2 pontos (faixa salarial e escolaridade)

    def test_candidatura_fields(self):
        """Verifica se os campos estão sendo armazenados corretamente"""
        self.assertEqual(self.candidatura.pretensao_salarial, 2500.00)
        self.assertEqual(self.candidatura.experiencia, "3 anos de experiência em Django.")
        self.assertEqual(self.candidatura.escolaridade, "superior")
        self.assertEqual(self.candidatura.candidato, self.usuario)
        self.assertEqual(self.candidatura.vaga, self.vaga)

class CandidaturaViewsTest(TestCase):
    def setUp(self):
        """Cria usuários, vagas e candidatos para os testes e configura o cliente"""
        self.client = Client()
        self.usuario = User.objects.create_user(username='candidato', password='senha')
        self.empresa = User.objects.create_user(username='empresa', password='senha')
        self.vaga = Vaga.objects.create(
            nome="Desenvolvedor Django",
            requisitos="Conhecimento avançado em Django e Python.",
            faixa_salarial="2000-3000",
            escolaridade_minima="superior"
        )
        self.candidatura_url = reverse('candidatar_vaga', args=[self.vaga.id])
        self.listar_vagas_url = reverse('listar_vagas_candidato')
        self.visualizar_candidaturas_url = reverse('visualizar_candidaturas', args=[self.vaga.id])

    def test_listar_vagas_candidato(self):
        """Verifica se a página de listar vagas está acessível e mostra as vagas"""
        self.client.login(username='candidato', password='senha')
        response = self.client.get(self.listar_vagas_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Desenvolvedor Django")

    def test_candidatar_vaga(self):
        """Verifica se o processo de candidatura está funcionando corretamente"""
        self.client.login(username='candidato', password='senha')
        response = self.client.post(self.candidatura_url,{
            'pretensao_salarial': 2500.00,
            'experiencia': '3 anos de experiência em Django.',
            'escolaridade': 'superior'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após salvar
        # Verifica se a candidatura foi salva no banco de dados
        self.assertTrue(Candidatura.objects.filter(
            candidato=self.usuario,
            vaga=self.vaga,
            pretensao_salarial=2500.00,
            experiencia='3 anos de experiência em Django.',
            escolaridade='superior'
        ).exists())


    def test_visualizar_candidaturas(self):
        """Verifica se a página de visualizar candidaturas está acessível e mostra as candidaturas"""
        # Primeiro, cria uma candidatura
        Candidatura.objects.create(
            candidato=self.usuario,
            vaga=self.vaga,
            pretensao_salarial=2500.00,
            experiencia="3 anos de experiência em Django.",
            escolaridade="superior"
        )
        self.client.login(username='empresa', password='senha')
        response = self.client.get(self.visualizar_candidaturas_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "candidato")

    def test_candidatar_vaga_already_applied(self):
        """Verifica se o sistema avisa quando o usuário já se candidatou à vaga"""
    # Cria uma candidatura inicial
        Candidatura.objects.create(
            candidato=self.usuario,
            vaga=self.vaga,
            pretensao_salarial=2500.00,
            experiencia="3 anos de experiência em Django.",
            escolaridade="superior"
        )
        self.client.login(username='candidato', password='senha')
        response = self.client.post(self.candidatura_url, {
            'pretensao_salarial': 3000.00,
            'experiencia': '4 anos de experiência em Django.',
            'escolaridade': 'superior'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após detectar a candidatura existente

        # Seguindo o redirecionamento
        response = self.client.get(response.url)
        self.assertContains(response, 'Você já se candidatou para essa vaga.')