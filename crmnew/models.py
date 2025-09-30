from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("sales_rep", "Sales Representative"),
        ("support", "Support Staff"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="sales_rep")

    def __str__(self):
        return f"{self.username} ({self.role})"



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Organization(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name



class Customer(BaseModel):

    name = models.CharField(max_length=50)
    organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name="customers"
    )

    def __str__(self):
        return self.name



class ContactInfo(models.Model):
    CONTACT_TYPE_CHOICES = [
        ("email", "Email"),
        ("phone", "Phone"),
        ("whatsapp", "WhatsApp"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="contact_infos")
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES)
    value = models.CharField(max_length=200)
    label = models.CharField(max_length=50, blank=True, null=True)  
    is_primary = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.customer.name} - {self.value} ({self.contact_type})" 
    
    
    def clean(self):
        if self.is_primary:
            qs = ContactInfo.objects.filter(customer=self.customer, is_primary=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk) 
            if qs.exists():
                raise ValidationError("This customer already has a primary contact.")

class Activity(BaseModel):
    ACTIVITY_TYPE_CHOICES = [
         
        ("email", "Email"),
        ("call", "Call"),
        ("whatsapp", "Whatsapp"),
        ("meeting", "Meeting"),
        
    ]

    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_to")

    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    notes = models.TextField(blank=True, null=True)
    scheduled_for = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.activity_type}"
    
class LeadStatus(models.Model):
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#808080")
    order = models.PositiveIntegerField(default=1,unique=True)
    def __str__(self):
        return self.label
    
class LeadStatusTransition(models.Model):
    from_status = models.ForeignKey(LeadStatus, on_delete=models.CASCADE, related_name="transitions_from")
    to_status = models.ForeignKey(LeadStatus, on_delete=models.CASCADE, related_name="transitions_to")

    class Meta:
        unique_together = ("from_status", "to_status")
    def __str__(self):
        return f"{self.from_status} → {self.to_status}"

class Lead(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="leads")
    status = models.ForeignKey(LeadStatus, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_leads")
    notes = models.TextField(blank=True, null=True)
    activities = models.ManyToManyField(Activity, blank=True, related_name="leads")
    def __str__(self):
        return f"{self.customer.name} ({self.status})"
    
    def clean(self):
        if self.pk and self.status:  
            old_status = Lead.objects.get(pk=self.pk).status
            if old_status and old_status != self.status:
                if not LeadStatusTransition.objects.filter(
                    from_status=old_status, to_status=self.status
                ).exists():
                    raise ValidationError(f"Invalid transition: {old_status} → {self.status}")
    

class DealStage(models.Model):
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=1,unique=True)
    color = models.CharField(max_length=7, default="#808080")
    def __str__(self):
        return self.label

class DealStageTransition(models.Model):
    from_stage = models.ForeignKey(DealStage, on_delete=models.CASCADE, related_name="transitions_from")
    to_stage = models.ForeignKey(DealStage, on_delete=models.CASCADE, related_name="transitions_to")

    class Meta:
        unique_together = ("from_stage", "to_stage")
    def __str__(self):
        return f"{self.from_stage} → {self.to_stage}"

class Deal(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="deals")
    stage = models.ForeignKey(DealStage, on_delete=models.SET_NULL, null=True, blank=True)
    expected_close_date = models.DateField(blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_deals")
    activities = models.ManyToManyField(Activity, blank=True, related_name="deals")
    def __str__(self):
        return f"Deal with {self.customer.name} - {self.stage}"

   

    
class TaskStatus(models.Model):  
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#808080")
    def __str__(self):
        return self.label
    
class Task(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True,related_name="created_tasks")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True, related_name="assigned_tasks")
     
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True, related_name="tasks")
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, null=True, blank=True)
    
    priority = models.CharField(max_length=10, choices=[("low", "Low"), ("medium", "Medium"),("high", "High"), ("urgent", "Urgent"),], default="medium")
    due_date = models.DateTimeField(blank=True, null=True)
    depends_on = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="dependent_tasks")

    def __str__(self):
        return f"{self.title} (Assigned to: {self.assigned_to})"

   
#activity-deal
#dealstage,task
#statusdynamic, contactmult 
#allowed stage transitions only