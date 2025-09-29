from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.utils import timezone


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



class Organization(BaseModel):
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



class ContactInfo(BaseModel):
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



class LeadStatus(models.Model):
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=1,unique=True)
    def __str__(self):
        return self.label

class Lead(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="leads")
    status = models.ForeignKey(LeadStatus, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_leads")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Lead: {self.customer.name} ({self.status})"

class DealStage(models.Model):
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=1,unique=True)
    def __str__(self):
        return self.label


class Deal(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="deals")
    stage = models.ForeignKey(DealStage, on_delete=models.SET_NULL, null=True, blank=True)
    expected_close_date = models.DateField(blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_deals")

    def __str__(self):
        return f"Deal with {self.customer.name} - {self.stage}"



class Activity(BaseModel):
    ACTIVITY_TYPE_CHOICES = [
         
        ("email", "Email"),
        ("call", "Call"),
        ("whatsapp", "Whatsapp"),
        ("meeting", "Meeting"),
        
    ]

    deal = models.ForeignKey(Deal, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="performed_activities")

    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    notes = models.TextField(blank=True, null=True)
    scheduled_for = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.activity_type} for {self.deal}"
    
class TaskStatus(models.Model):  
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=1,unique=True)
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

    def __str__(self):
        return f"{self.title} (Assigned to: {self.assigned_to})"

   
#activity-deal
#dealstage,task
#statusdynamic, contactmult 
#allowed stage transitions only