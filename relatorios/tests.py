from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils import timezone
from vagas.models import Vaga
from candidaturas.models import Candidatura

class RelatoriosViewsTest(TestCase):
    def setUp(self):
        self.empresa_group = Group.objects.create(name='empresa', id='2')
        self.user = User.objects.create_user(username='empresa@example.com', password='senha')
        self.empresa_group.user_set.add(self.user)
        
        self.client = Client()
        self.client.login(username='empresa@example.com', password='senha')

        self.inicial_url = reverse('inicial')
        self.vagas_criadas_por_mes_url = reverse('vagas_criadas_por_mes')
        self.candidatos_recebidos_por_mes_url = reverse('candidatos_recebidos_por_mes')
        self.relatorios_url = reverse('relatorios')

        # Cria dados de teste
        self.vaga = Vaga.objects.create(
            nome='Vaga de Teste',
            requisitos='Requisitos da vaga.',
            faixa_salarial='2000-3000',
            escolaridade_minima='superior',
            criado_em=timezone.now()
        )
        self.candidatura = Candidatura.objects.create(
            vaga=self.vaga,
            candidato=self.user,
            data_candidatura=timezone.now(),
            pretensao_salarial=3000.00  # Adiciona o valor necessário
        )

    def test_inicial(self):
        response = self.client.get(self.inicial_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inicial.html')

    def test_vagas_criadas_por_mes(self):
        response = self.client.get(self.vagas_criadas_por_mes_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            timezone.now().strftime('%m-%Y'): 1
        })

    def test_candidatos_recebidos_por_mes(self):
        response = self.client.get(self.candidatos_recebidos_por_mes_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            timezone.now().strftime('%m-%Y'): 1
        })

    def test_relatorios(self):
        response = self.client.get(self.relatorios_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'relatorios.html')

    def test_custom_logout(self):
        response = self.client.get(reverse('custom_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
