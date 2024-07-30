from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
   path('inicial/', views.inicial, name='inicial'),
   path('api/vagas_criadas_por_mes/', views.vagas_criadas_por_mes, name='vagas_criadas_por_mes'),
   path('api/candidatos_recebidos_por_mes/', views.candidatos_recebidos_por_mes, name='candidatos_recebidos_por_mes'),
   path('relatorios/', views.relatorios, name='relatorios'),
   path('logout/', views.custom_logout, name='custom_logout')

]

