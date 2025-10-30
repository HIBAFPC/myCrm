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
from django.db.models.signals import pre_save
from .models import Lead
from .tasks import send_lead_converted_email
from .tasks import send_assigned_email

@receiver(pre_save, sender=Lead)
def send_conversion_notification(sender, instance, **kwargs):
    
    if not instance.pk:
        
        return

    try:
        old_instance = Lead.objects.get(pk=instance.pk)
    except Lead.DoesNotExist:
        return

    
    if not old_instance.is_converted and instance.is_converted:
        assigned_user = instance.assigned_to
        if assigned_user and assigned_user.email:
            send_lead_converted_email.delay(
                lead_name=instance.name,
                user_email=assigned_user.email
            )
from .tasks import send_assigned_email  
from crmnew.models import Lead, Task, Deal

ASSIGNMENT_MODELS = {
    Lead: "Lead",
    Task: "Task",
    Deal: "Deal",
}

@receiver(pre_save)
def store_old_assigned_user(sender, instance, **kwargs):
    if sender not in ASSIGNMENT_MODELS:
        return
    if not instance.pk:
        instance._old_assigned_to = None
        return
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        instance._old_assigned_to = old_instance.assigned_to
    except sender.DoesNotExist:
        instance._old_assigned_to = None


@receiver(post_save)
def handle_assignment(sender, instance, created, **kwargs):
    if sender not in ASSIGNMENT_MODELS:
        return
 
    if not hasattr(instance, "assigned_to") or not instance.assigned_to:
        return
    model_name = ASSIGNMENT_MODELS[sender]

    
    if created or getattr(instance, "_old_assigned_to", None) != instance.assigned_to:
        send_assigned_email.delay(
            object_name=model_name,
            item_name=getattr(instance, "name", str(instance)),
            user_email=instance.assigned_to.email,
        )
        print(f"📩 {model_name} '{instance}' assigned to {instance.assigned_to.email}")