from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError



class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    
class UserType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, blank=True)
    
    def __str__(self):
        return self.label


class User(AbstractUser):
    
    user_type = models.ForeignKey(
        "UserType", on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
    def __str__(self): 
      return f"{self.username} ({self.user_type})"

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

        
class ActivityType(models.Model):
    code = models.CharField(max_length=50, unique=True,default='email')   
    label = models.CharField(max_length=100,default='Email')              

    def __str__(self):
        return self.label


class Activity(BaseModel):
    title = models.CharField(max_length=200,default="Contact")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_activities")
    activity_type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True, blank=False, related_name="activities")
    notes = models.TextField(blank=True, null=True)
    scheduled_for = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.activity_type})"
    
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
    name = models.CharField(max_length=50)
    organizations = models.ManyToManyField('Organization', blank=True, related_name="leads" )
    qualification = models.CharField(max_length=200, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    
    status = models.ForeignKey(LeadStatus, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_leads")
    notes = models.TextField(blank=True, null=True)
    activities = models.ManyToManyField(Activity, blank=True, related_name="leads")
    next_followup = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({self.status.label if self.status else 'No Status'})"
    
    def clean(self):
        if self.pk and self.status:  
            old_status = Lead.objects.get(pk=self.pk).status
            if old_status and old_status != self.status:
                if not LeadStatusTransition.objects.filter(
                    from_status=old_status, to_status=self.status
                ).exists():
                    raise ValidationError(f"Invalid transition: {old_status} → {self.status}")
                
class ContactInfo(models.Model):

    class ContactType(models.TextChoices):
        EMAIL = "email", "Email"
        PHONE = "phone", "Phone"
        WHATSAPP = "whatsapp", "WhatsApp"

    lead = models.ForeignKey('Lead', on_delete=models.CASCADE, related_name="contact_infos")
    contact_type = models.CharField( max_length=20, choices=ContactType.choices,)
    value = models.CharField(max_length=200)
    label = models.CharField(max_length=50, blank=True, null=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.lead.name} - {self.value} ({self.get_contact_type_display()})"

    def clean(self):
        if self.is_primary:
            qs = ContactInfo.objects.filter(lead=self.lead, is_primary=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("This lead already has a primary contact.")
  
class Student(BaseModel):
    lead = models.OneToOneField( Lead,on_delete=models.CASCADE, related_name="student")
    enrollment_date = models.DateField(default=timezone.now)
    student_id = models.CharField(max_length=50, unique=True)
    course = models.CharField(max_length=200, blank=True, null=True) 

    def __str__(self):
        return f"{self.lead.name} (Student ID: {self.student_id})"

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
    title = models.CharField(max_length=200,default="Untitled Deal")
    customer = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="deals")
    stage = models.ForeignKey(DealStage, on_delete=models.SET_NULL, null=True, blank=True)
    expected_close_date = models.DateField(blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_deals")
    activities = models.ManyToManyField(Activity, blank=True, related_name="deals")
    def __str__(self):
        return f"{self.title} with {self.customer.name} - ({self.stage.label if self.stage else 'No Stage'})"
    
    def clean(self):
        if self.pk and self.stage:  
            old_stage = Deal.objects.get(pk=self.pk).stage
            if old_stage and old_stage != self.stage:
                if not DealStageTransition.objects.filter(
                    from_stage=old_stage, to_stage=self.stage
                ).exists():
                    raise ValidationError(f"Invalid transition: {old_stage} → {self.stage}")
    
    
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
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
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