from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and obj.id == request.user.id:
            return True
        elif request.user.is_authenticated and request.user.is_superuser:
            return True
        else:
            return False 
        