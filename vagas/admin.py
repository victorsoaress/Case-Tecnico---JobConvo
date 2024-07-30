from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Vaga

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'faixa_salarial', 'escolaridade_minima', 'criado_em', 'modificado_em')
    search_fields = ('nome', 'requisitos')
    list_filter = ('faixa_salarial', 'escolaridade_minima')
