from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Matricula, Mensalidade


@receiver(post_save, sender=Matricula)
def create_auth_token_aluno(sender, instance=None, created=False, **kwargs):
    if created:
        Mensalidade.objects.generate_mensalidades(instance)
