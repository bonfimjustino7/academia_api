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

    def clean_email(self):
        User = get_user_model()

        if not self.instance.pk: # quando não existir
            if User.objects.filter(email=self.cleaned_data.get('email')).exists():
                self.add_error('email', 'Este email já está sendo usado por outro usuário')
        else:
            if self.data.get('email') != self.instance.user.email and User.objects.filter(email=self.cleaned_data.get('email')).exists():
                self.add_error('email', 'Este email já está sendo usado por outro usuário')

        return self.cleaned_data.get('email')

    class Meta:
        model = DadosBasicos
        fields = ('nome', 'endereco', 'email', 'password', 'telefone')

    def save(self, commit=True):
        User = get_user_model()

        if not self.instance.pk:
            user = User.objects.create_user(username=self.data.get('nome'),
                                            email=self.data.get('email'),
                                            password=self.data.get('password')
                                            )
            self.instance.user = user
        else:
            user = self.instance.user
            user.username = self.data.get('nome')
            user.email = self.data.get('email')
            if self.data.get('password'):
                user.set_password(self.data.get('password'))

            user.save()
        return super(DadosBasicosForm, self).save(commit)


class AlunoForm(DadosBasicosForm):
    cpf = forms.CharField(max_length=11, required=False)


class AcademiaForm(DadosBasicosForm):
    cnpj = forms.CharField(max_length=14, required=False)
