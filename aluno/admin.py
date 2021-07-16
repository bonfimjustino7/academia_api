from . import forms
from django.contrib import admin
from .models import Aluno


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    form = forms.AlunoForm
    fields = ('nome', 'email', ('password', 'password2'), 'telefone', 'cpf', 'endereco')
