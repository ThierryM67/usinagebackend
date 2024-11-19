from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Request, Rating


@receiver(post_save, sender=Request)
def create_rating(sender, instance, created, **kwargs):
    if created:
        Rating.objects.create(request=instance)

# @receiver(post_save, sender=Request)
# def save_rating(sender, instance, **kwargs):
#     instance.rating.save()