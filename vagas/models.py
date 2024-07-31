from django.db import models

# vagas/models.py

class Vaga(models.Model):
    FAIXA_SALARIAL_CHOICES = [
        ('0-1000', 'Até 1.000'),
        ('1000-2000', 'De 1.000 a 2.000'),
        ('2000-3000', 'De 2.000 a 3.000'),
        ('3000-100000', 'Acima de 3.000'),
    ]

    ESCOLARIDADE_CHOICES = [
        ('fundamental', 'Ensino fundamental'),
        ('medio', 'Ensino médio'),
        ('tecnologo', 'Tecnólogo'),
        ('superior', 'Ensino Superior'),
        ('pos', 'Pós / MBA / Mestrado'),
        ('doutorado', 'Doutorado'),
    ]
    nome = models.CharField(max_length=200, verbose_name='Nome da vaga')
    requisitos = models.TextField(verbose_name='Requisitos')
    faixa_salarial = models.CharField(max_length=15,choices=FAIXA_SALARIAL_CHOICES, verbose_name='Faixa salarial')
    escolaridade_minima = models.CharField(max_length=20, choices=ESCOLARIDADE_CHOICES, verbose_name='Escolaridade mínima')
    status = models.CharField(default='ativo',max_length=10)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.nome

  