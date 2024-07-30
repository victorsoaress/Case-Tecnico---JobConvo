from django.urls import path, include
from . import views

urlpatterns = [
   path('auth/', include('usuarios.urls')),
   path('', views.home, name='home'),
   path('vagas/', include('vagas.urls'))
]
