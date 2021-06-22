from django.contrib import admin
from core.models import Academia, Aluno
from . import forms


@admin.register(Academia)
class AcademiaAdmin(admin.ModelAdmin):
    form = forms.AcademiaForm
    fields = ('nome', 'email', ('password', 'password2'), 'telefone', 'cnpj', 'endereco')


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    form = forms.AlunoForm
    fields = ('nome', 'email', ('password', 'password2'), 'telefone', 'cpf', 'endereco')


