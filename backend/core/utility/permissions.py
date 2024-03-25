from rest_framework.permissions import BasePermission

class CustomPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == "OPTIONS":
            return True
        else:
            return bool(request.user and request.user.is_authenticated)