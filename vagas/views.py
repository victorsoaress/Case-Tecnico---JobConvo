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
def criarvagas(request):
    if request.method == 'POST':
        form=VagaForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request,'Vaga criada com sucesso')
                return redirect ('criarvagas')
    else:
            form=VagaForm()
    return render(request, 'criarvagas.html', {'form':form})

@empresa_required
@login_required
def listarvagasadm(request):
      vagas = Vaga.objects.annotate(num_candidaturas=Count('candidatura'))
      return render(request, 'listarvagasadm.html',{'vagas':vagas})

@empresa_required
@login_required
def deletar_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)
    
    if request.method == 'POST':
        vaga.delete()
        return redirect('listarvagasadm')  
    
    return redirect('listarvagasadm')

@empresa_required
@login_required
def editarvaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)

    if request.method == 'POST':
          form = VagaForm(request.POST, instance=vaga)
          if form.is_valid(): 
               form.save()
               return redirect('listarvagasadm')
    else: 
        form = VagaForm(instance=vaga)
    return render(request, 'editarvaga.html', {'form':form, 'vaga':vaga})