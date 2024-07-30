
# Create your tests here.
from django.test import TestCase
from django.urls import reverse

class HomeViewTests(TestCase):
    def test_home_status_code(self):
        """Testa se a página home retorna um status code 200"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_template_used(self):
        """Testa se a página home usa o template correto"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')