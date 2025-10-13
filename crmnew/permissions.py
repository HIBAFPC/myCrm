
from rest_framework.permissions import BasePermission

class AuthDocPermission(BasePermission):


    def has_permission(self, request, view):
        required = getattr(view, "required_permissions", [])
        if not required:
            return True  

        user_perms = request.user.get_all_permissions()  
        return all(perm in user_perms for perm in required)
