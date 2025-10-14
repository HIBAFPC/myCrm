
# from rest_framework.permissions import BasePermission

# class AuthDocPermission(BasePermission):


#     def has_permission(self, request, view):
#         required = getattr(view, "required_permissions", [])
#         if not required:
#             return True  

#         user_perms = request.user.get_all_permissions()  
#         return all(perm in user_perms for perm in required)
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
        
#         # for permission in required_permissions:
#         #     has_permission = user.user_type.permissions.filter(code=permission).exists() 
#         #     if not has_permission:
#         #        return False  

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
    """
    Custom permission to check if the requesting user has the required permissions.
    Works with UserType → Permission relationship.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Superusers bypass all permission checks
        if user.is_superuser:
            return True

        # Dynamically get required permissions for this view/method
        required_permissions = getattr(view, 'required_permissions', [])

        # If a dict mapping HTTP methods to permissions is used
        if isinstance(required_permissions, dict):
            required_permissions = required_permissions.get(request.method, [])

        if not required_permissions:
            return True  # No permissions required

        # Check if user_type has all required permissions
        user_type_perms = user.user_type.permissions.values_list('code', flat=True) if user.user_type else []

        for perm in required_permissions:
            if perm not in user_type_perms:
                return False  # Deny immediately if any required permission is missing

        return True
