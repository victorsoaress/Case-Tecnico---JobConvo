from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Count
from vagas.models import Vaga 
from candidaturas.models import Candidatura
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from usuarios.decorators import empresa_required

# Create your views here.
@empresa_required
@login_required
def inicial(request):
    return render(request, 'inicial.html')

@empresa_required
@login_required
def vagas_criadas_por_mes(request):
    try:
        data = (Vaga.objects.annotate(mes=TruncMonth('criado_em'))
                .values('mes')
                .annotate(count=Count('id'))
                .order_by('mes'))
        data_dict = {item['mes'].strftime('%m-%Y'): item['count'] for item in data}
        return JsonResponse(data_dict)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@empresa_required
@login_required
def candidatos_recebidos_por_mes(request):
    try:
        data = (Candidatura.objects.annotate(mes=TruncMonth('data_candidatura'))
                .values('mes')
                .annotate(count=Count('id'))
                .order_by('mes'))
        data_dict = {item['mes'].strftime('%m-%Y'): item['count'] for item in data}
        return JsonResponse(data_dict)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@empresa_required
@login_required
def relatorios(request):
    return render(request, 'relatorios.html')

def custom_logout(request):
    logout(request)  # Desloga o usuário
    return redirect('home')