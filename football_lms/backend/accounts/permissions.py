from rest_framework.permissions import BasePermission

class IsAdminOrCoachOrStaff(BasePermission):
    def has_permission(self, request, view):
        # Allow access to the resource if the user is an admin, coach, or staff
        return request.user.is_authenticated and request.user.role in ['admin', 'coach', 'staff']
