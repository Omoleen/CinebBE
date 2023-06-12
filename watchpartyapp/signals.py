from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=PartyGroup)
def create_rider_profile(sender, instance, created, **kwargs):
    if created:
        PartyGroupMessage.objects.create(partyGroup=instance, message='Group created!', message_from_machine=True)