from django import forms
from academia.forms import DadosBasicosForm


class AlunoForm(DadosBasicosForm):
    cpf = forms.CharField(max_length=14, required=False)
