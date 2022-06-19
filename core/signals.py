from .models import Cases, Recon
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Cases)
def create_recon_table(sender, instance, created, **kwargs):
    if created:
        Recon.objects.create(case=instance)


@receiver(post_save, sender=Cases)
def save_cases(sender, instance, **kwargs):
    instance.recon.save()
