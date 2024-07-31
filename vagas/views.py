# users/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Vaga
from .forms import VagaForm
from django.db.models import Count
from usuarios.decorators import empresa_required
from django.contrib import messages  

@empresa_required
@login_required
def criar_vagas(request):
    if request.method == 'POST':
        form=VagaForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request,'Vaga criada com sucesso')
                return redirect ('criar_vagas')
    else:
            form=VagaForm()
    return render(request, 'criar_vagas.html', {'form':form})

@empresa_required
@login_required
def listar_vagas_adm(request):
      vagas = Vaga.objects.annotate(num_candidaturas=Count('candidatura'))
      return render(request, 'listar_vagas_adm.html',{'vagas':vagas})

@empresa_required
@login_required
def deletar_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)
    
    if request.method == 'POST':
        vaga.delete()
        return redirect('listar_vagas_adm')  
    
    return redirect('listar_vagas_adm')

@empresa_required
@login_required
def editar_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)

    if request.method == 'POST':
          form = VagaForm(request.POST, instance=vaga)
          if form.is_valid(): 
               form.save()
               return redirect('listar_vagas_adm')
    else: 
        form = VagaForm(instance=vaga)
    return render(request, 'editar_vaga.html', {'form':form, 'vaga':vaga})

def encerrar_vaga(request,id):
    vaga = get_object_or_404(Vaga, id=id)
    if request.method == 'POST':
        vaga.status='encerrada'
        vaga.save()
        return redirect('listar_vagas_adm')  
    
    return redirect('listar_vagas_adm')