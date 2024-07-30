# **Case Técnico - JobConvo**
## Este projeto tem como objetivo criar um sistema de gerenciamento de vagas de emprego usando Python 3.12.4 e Django 5.0.7. 
O sistema permite que empresas cadastrem vagas e candidatos se candidatem a elas. Além disso, inclui funcionalidades para geração de relatórios gráficos com o Charts.js.

##Funcionalidades
--Cadastro de usuários com email e senha.
--Criação, edição e exclusão de vagas por empresas.
--Candidatura de usuários a vagas.
--Visualização de candidatos por vaga.
--Relatórios gráficos de vagas criadas por mês e candidatos recebidos por mês.

##Pré-requisitos:
--VsCode(ou outro compilador)
--Python
--pip (gerenciador de pacotes do Python)
--virtualenv (opcional, mas recomendado)

##Para rodar o projeto

###Abra o terminal e digite:

```
git clone https://github.com/victorsoaress/Case-Tecnico---JobConvo.git
cd Case-Tecnico---JobConvo

```

###Crie um ambiente virtual 

```
python -m venv venv
cd venv\Scripts\activate
```
###Instale todas as dependências necessárias
```
pip install -r requirements.txt
```
###Configure o banco de dados
```
python manage.py makemigrations
```
```
python manage.py migrate
```
###Caso queira, está disponibilizado um BD para teste. Com 2 usuários cadastros e 4 vagas criadas.
Login Candidato:
email = usuario@candidato.com
senha = Candidato12#
Login Empresa:
email = usuario@empresa.com
senha = Empresa12#

Para carregar o banco:

```
python manage.py loaddata db_teste.json

```

###Rode o software em ambiente local
```
python manage.py runserver
```


