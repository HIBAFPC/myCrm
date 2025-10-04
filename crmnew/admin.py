from django.contrib import admin

# Register your models here.
from .models import User, Organization, Lead, LeadStatus, Deal, DealStage, Activity, TaskStatus, Task, ContactInfo, LeadStatusTransition, DealStageTransition, ActivityType,Student

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Lead)
admin.site.register(LeadStatus)
admin.site.register(Deal)
admin.site.register(DealStage)
admin.site.register(Activity)
admin.site.register(TaskStatus)
admin.site.register(Task)
admin.site.register(ContactInfo)
admin.site.register(LeadStatusTransition)
admin.site.register(DealStageTransition)
admin.site.register(ActivityType)
admin.site.register(Student)