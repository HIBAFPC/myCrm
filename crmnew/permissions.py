

# from rest_framework.permissions import BasePermission


# class HasCustomPermission(BasePermission):

#     def has_permission(self, request, view):
#         required_permissions = getattr(view, 'required_permissions', None)
        
#         if isinstance(required_permissions, str):
#             required_permissions = [required_permissions] 

#         if not required_permissions:
#             return True
        
#         user = request.user

#         if not user or not user.is_authenticated:
#             return False

#         if user.is_superuser:
#             return True
        
#         for perm in required_permissions:
#             if not user.user_type.permissions.filter(code=perm).exists():
#                 return False
        
# 

#         return True

#         count = 0
#         for permission in required_permissions:
#             role_permission_qs = user.user_type.permissions.filter(name=permission) if user.user_type else None
            

#             if role_permission_qs and role_permission_qs.exists() :
#                 count = count + 1

#         if count == len(required_permissions): 
#             return True

#         return False
from rest_framework.permissions import BasePermission

class HasCustomPermission(BasePermission):
    

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

       
        if user.is_superuser:
            return True

        
        required_permissions = getattr(view, 'required_permissions', [])

        
        if isinstance(required_permissions, dict):
            required_permissions = required_permissions.get(request.method, [])

        if not required_permissions:
            return True  

        
        user_type_perms = user.user_type.permissions.values_list('code', flat=True) if user.user_type else []

        for perm in required_permissions:
            if perm not in user_type_perms:
                return False  

        return True
    
    
    
class IsLeadOwnerOrAdmin(BasePermission):
    

    def has_object_permission(self, request, view, obj):
       
        lead = obj.lead

        
        if request.user.is_staff or request.user.is_superuser:
            return True

        
        return lead.assigned_to == request.user

    def has_permission(self, request, view):
        
        return request.user and request.user.is_authenticated