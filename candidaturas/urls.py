from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('listar_vagas_candidato/', views.listar_vagas_candidato, name='listar_vagas_candidato'),
    path('candidatar_vaga/<int:id>', views.candidatar_vaga, name='candidatar_vaga'),
    path('visualizar_candidaturas/<int:id>/', views.visualizar_candidaturas, name='visualizar_candidaturas'),
    path('logout/', views.custom_logout, name='logout')
]
