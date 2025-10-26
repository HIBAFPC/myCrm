from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import *

# admin.site.register(User)
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
admin.site.register(Permission)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "first_name", "last_name", "user_type", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "user_type")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "user_type","email","password1", "password2", "is_staff", "is_active")}
        ),
    )
    search_fields = ("username", "email")
    ordering = ("username",)

@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "label")