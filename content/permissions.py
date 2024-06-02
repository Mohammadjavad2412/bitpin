from rest_framework.permissions import BasePermission

class OnlyAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user and request.user.is_superuser:
                return True
            return False
        except:
            return False
