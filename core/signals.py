from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Academia, TokenAcademia


@receiver(post_save, sender=Academia)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        TokenAcademia.objects.create(user=instance)