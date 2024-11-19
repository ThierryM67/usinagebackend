from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Offer, Rating


@receiver(post_save, sender=Offer)
def create_rating(sender, instance, created, **kwargs):
    if created:
        Rating.objects.create(offer=instance)

# @receiver(post_save, sender=Offer)
# def save_rating(sender, instance, **kwargs):
#     instance.rating.save()