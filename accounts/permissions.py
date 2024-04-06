from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class BasePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in.")
        if not request.user.email_verified:
            raise PermissionDenied("Your email is not verified.")
        if not request.user.phone_verified:
            raise PermissionDenied("Your phone is not verified.")
        return True

class IsDriver(BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.verified_driver
