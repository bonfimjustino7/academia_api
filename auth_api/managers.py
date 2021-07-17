from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserManager(models.Manager):
    def create_user(self, **fields):

        user = User.objects.create_user(username=fields.pop('nome'),
                                        email=fields.pop('email'),
                                        password=fields.pop('password')
                                        )
        fields['user'] = user

        aluno = self.model.objects.create(**fields)

        return aluno