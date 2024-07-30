from django.urls import path, include
from . import views

urlpatterns = [
    path('criarvagas/', views.criarvagas, name='criarvagas'),
    path('listarvagasadm/', views.listarvagasadm, name = 'listarvagasadm'),
    path('deletar_vaga/<int:id>/', views.deletar_vaga, name='deletar_vaga'),
    path('editarvaga/<int:id>/', views.editarvaga, name='editarvaga'),
]
