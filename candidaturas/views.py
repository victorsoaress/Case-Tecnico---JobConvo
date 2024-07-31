from django.shortcuts import render, get_object_or_404, redirect
from .models import Candidatura
from .forms import CandidaturaForm
from vagas.models import Vaga
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from usuarios.decorators import empresa_required



@login_required
def listar_vagas_candidato(request):
    vagas = Vaga.objects.filter(status='ativo')
    return render (request, 'listar_vagas_candidato.html', {'vagas':vagas})

@login_required
def candidatar_vaga(request,id):
    vaga = get_object_or_404(Vaga, id=id)
    if Candidatura.objects.filter(candidato=request.user, vaga=vaga).exists():
        messages.warning(request, 'Você já se candidatou para essa vaga.')
        return redirect('listar_vagas_candidato')
    
    if request.method == 'POST':
        form = CandidaturaForm(request.POST)
        if form.is_valid():
            candidatura = form.save(commit=False)
            candidatura.candidato = request.user
            candidatura.vaga = vaga
            candidatura.save()
            return redirect ('listar_vagas_candidato')
    else:
        form = CandidaturaForm()
        return render (request,'candidatar_vaga.html', {'form':form, 'vaga':vaga})

@empresa_required
@login_required
def visualizar_candidaturas(request, id):
    vaga = get_object_or_404(Vaga, id=id)
    candidaturas = Candidatura.objects.filter(vaga = vaga).select_related('candidato')
    return render(request, 'visualizar_candidaturas.html', {'vaga':vaga, 'candidaturas':candidaturas})

def custom_logout(request):
    logout(request) 
    return redirect('home')

