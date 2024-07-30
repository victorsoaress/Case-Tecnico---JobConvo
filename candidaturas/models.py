from django.db import models
from django.contrib.auth.models import User
from vagas.models import Vaga
# Create your models here.

class Candidatura(models.Model):
    candidato = models.ForeignKey(User, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    pretensao_salarial = models.DecimalField(max_digits=10, decimal_places=2)
    experiencia = models.TextField()
    escolaridade = models.CharField(max_length=20, choices=[
        ('fundamental', 'Ensino fundamental'),
        ('medio', 'Ensino médio'),
        ('tecnologo', 'Tecnólogo'),
        ('superior', 'Ensino Superior'),
        ('pos', 'Pós / MBA / Mestrado'),
        ('doutorado', 'Doutorado'),
    ])
    data_candidatura = models.DateTimeField(auto_now_add=True)

    def calcular_pontuacao(self):
        pontos = 0
        escolaridades = ['fundamental','medio','tecnologo','superior','pos','doutorado']
        vaga_min_salario, vaga_max_salario = map(float, self.vaga.faixa_salarial.split('-'))

        if self.pretensao_salarial >= vaga_min_salario and self.pretensao_salarial <= vaga_max_salario :
            pontos +=1

        if escolaridades.index(self.escolaridade) >= escolaridades.index(self.vaga.escolaridade_minima):
            pontos +=1

        print(vaga_max_salario, vaga_min_salario, self.pretensao_salarial)

        return pontos
        
    def __str__(self):
        return f"{self.candidato.username} - {self.vaga.nome}"