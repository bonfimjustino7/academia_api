from django import forms
from django.contrib.auth import get_user_model

from .models import Aluno, DadosBasicos


class DadosBasicosForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DadosBasicosForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.fields['nome'].initial = kwargs.get('instance').user.username
            self.fields['email'].initial = kwargs.get('instance').user.email
        else:
            self.fields['password'].required = True
            self.fields['password2'].required = True

    nome = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label='Nova Senha', required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar Senha', required=False)
    endereco = forms.CharField(required=False)

    def clean_password(self):
        senha = self.cleaned_data.get('password')
        senha2 = self.cleaned_data.get('password2')

        if senha and senha2 and senha != senha2:
            self.add_error('password', 'Senhas não conhecidem')

        return senha

    class Meta:
        model = DadosBasicos
        fields = ('nome', 'endereco', 'email', 'password', 'telefone')

    def save(self, commit=True):
        User = get_user_model()
        user = User.objects.filter(email=self.data.get('email')).last()
        if not user:
            user = User.objects.create_user(username=self.data.get('nome'),
                                            email=self.data.get('email'),
                                            password=self.data.get('password')
                                            )
        else:
            user.username = self.data.get('nome')
            user.email = self.data.get('email')
            if self.data.get('password'):
                user.set_password(self.data.get('password'))

            user.save()
        self.instance.user = user
        return super(DadosBasicosForm, self).save(commit)


class AlunoForm(DadosBasicosForm):
    cpf = forms.CharField(max_length=11, required=False)


class AcademiaForm(DadosBasicosForm):
    cnpj = forms.CharField(max_length=14, required=False)
