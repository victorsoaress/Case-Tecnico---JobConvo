from django.urls import path, include
from . import views

urlpatterns = [
    path('criar_vagas/', views.criar_vagas, name='criar_vagas'),
    path('listar_vagas_adm/', views.listar_vagas_adm, name = 'listar_vagas_adm'),
    path('deletar_vaga/<int:id>/', views.deletar_vaga, name='deletar_vaga'),
    path('editar_vaga/<int:id>/', views.editar_vaga, name='editar_vaga'),
    path('encerrar_vaga/<int:id>', views.encerrar_vaga, name='encerrar_vaga')

]
