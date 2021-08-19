from . import forms
from django.contrib import admin
from .models import Aluno, Medicao


class MedicoesAdmin(admin.StackedInline):
    model = Medicao
    readonly_fields = ('data_criacao',)
    fields = ("data_criacao",
              "peso",
              "altura",
              "braco_direito",
              "braco_esquerdo",
              "antebraco_direito",
              "antebraco_esquerdo",
              "ombro",
              "peitoral",
              "abdome",
              "cintura",
              "gluteo",
              "coxa_direita",
              "coxa_esquerda",
              "panturrilha_direta",
              "panturrilha_esquerda",
              "aluno",)
    can_delete = False
    extra = 0


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    form = forms.AlunoForm
    inlines = [MedicoesAdmin]
    fields = ('nome', 'email', ('password', 'password2'), 'telefone', 'cpf', 'endereco')
