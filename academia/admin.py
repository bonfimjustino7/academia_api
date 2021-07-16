from . import forms
from django.contrib import admin
from .models import Academia


@admin.register(Academia)
class AcademiaAdmin(admin.ModelAdmin):
    form = forms.AcademiaForm
    fields = ('nome', 'email', ('password', 'password2'), 'telefone', 'cnpj', 'endereco')
