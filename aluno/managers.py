from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class AlunoManager(models.Manager):
    def create_aluno(self, **fields):
        from aluno.models import Aluno

        user = User.objects.create_user(username=fields.pop('nome'),
                                        email=fields.pop('email'),
                                        password=fields.pop('password')
                                        )
        fields['user'] = user

        aluno = Aluno.objects.create(**fields)

        return aluno