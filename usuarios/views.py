from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from rolepermissions.roles import assign_role
from django.contrib import messages  
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError




def cadastro(request):
   if request.method == "POST":
      email = request.POST.get('email')
      nome = request.POST.get('nome')
      senha = request.POST.get('senha')
      tipo = request.POST.get('tipo')
      user = User.objects.filter(username=email).exists()  
      if user:
         messages.error(request,'Usuário já cadastrado no sistema.')
         return redirect('cadastro')
      try: 
            validar_senha(senha)
            criar_usuario(email, nome, senha, tipo)
            return redirect ('login')
      except ValidationError as e:
         for error in e.messages:
            messages.error(request, error)
         return redirect('cadastro')
         
   return render(request, 'cadastro.html') 
   
def login(request):
   if request.method == "POST":
      email = request.POST.get('email')
      senha = request.POST.get('senha')
      user = authenticate(request, username=email, password=senha)

      if user is not None:
         login_django(request,user)
         return redirecionar_usuario(user)
      else:
         messages.error(request,'E-mail ou senha inválidos.')
         return redirect('login')

   return render(request, 'login.html')
   
def criar_usuario(email,nome,senha,tipo):
   user = User.objects.create_user(username=email, first_name=nome, password=senha)
   user.save()
   if tipo == 'Empresa':
      assign_role(user,'empresa')
   else:
      assign_role(user,'candidato')
   return user

def validar_senha(senha):
   try:
      validate_password(senha)
   except ValidationError as e:
      raise e
   
def redirecionar_usuario(user):
    urls = {
        'candidato': 'listar_vagas_candidato',
        'empresa': 'inicial',
    }
    for group_name, url in urls.items():
        if user.groups.filter(name=group_name).exists():
            return redirect(url)
    return redirect('login')
