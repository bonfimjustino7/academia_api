from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class AcademiaManager(models.Manager):
    def create_academia(self, **fields):
        from academia.models import Academia
        
        user = User.objects.create_user(username=fields.pop('nome'),
                                        email=fields.pop('email'),
                                        password=fields.pop('password')
                                        )
        fields['user'] = user

        aluno = Academia.objects.create(**fields)

        return aluno