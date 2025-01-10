from juntagrico.signals import member_created
from django.dispatch import receiver
from juntagrico.entity.member import Member


@receiver(member_created, sender=Member)
def create_member(sender, signal, instance, **kwargs):
    firstName = instance.first_name
    lastName = instance.last_name
    lastName = instance.email
