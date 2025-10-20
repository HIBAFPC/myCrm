# crmnew/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import User

@receiver(post_save, sender=User)
def assign_group_to_user(sender, instance, created, **kwargs):
    
    if created and instance.user_type:
        group, _ = Group.objects.get_or_create(name=instance.user_type.label)
        instance.groups.add(group)
