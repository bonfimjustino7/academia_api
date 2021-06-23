from django.contrib import admin
from core.models import Academia, Aluno
from django.contrib.auth.admin import UserAdmin

from . import forms
from .models import UserCustom


@admin.register(Academia)
class AcademiaAdmin(admin.ModelAdmin):
    form = forms.AcademiaForm
    fields = ('nome', 'email', ('password', 'password2'), 'telefone', 'cnpj', 'endereco')


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    form = forms.AlunoForm
    fields = ('nome', 'email', ('password', 'password2'), 'telefone', 'cpf', 'endereco')


@admin.register(UserCustom)
class UserAdmin(UserAdmin):
    pass

admin.site.site_header = 'Academia ADMIN'
admin.site.site_title = 'Academia ADMIN'
