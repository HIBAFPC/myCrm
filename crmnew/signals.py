# crmnew/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.contrib.auth.models import Group
# from .models import User

# @receiver(post_save, sender=User)
# def assign_group_to_user(sender, instance, created, **kwargs):
    
#     if created and instance.user_type:
#         group, _ = Group.objects.get_or_create(name=instance.user_type.label)
#         instance.groups.add(group)
# from django.db.models.signals import pre_save
# from .models import Lead
# from .tasks import send_lead_converted_email

# @receiver(pre_save, sender=Lead)
# def send_conversion_notification(sender, instance, **kwargs):
    
#     if not instance.pk:
        
#         return

#     try:
#         old_instance = Lead.objects.get(pk=instance.pk)
#     except Lead.DoesNotExist:
#         return

    
#     if not old_instance.is_converted and instance.is_converted:
#         assigned_user = instance.assigned_to
#         if assigned_user and assigned_user.email:
#             send_lead_converted_email.delay(
#                 lead_name=instance.name,
#                 user_email=assigned_user.email
#             )
