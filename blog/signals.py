from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea un Profile automáticamente cuando se crea un User."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Asegura que el profile se guarde cuando el User se guarde."""
    profile = getattr(instance, 'profile', None)
    if profile is not None:
        profile.save()
