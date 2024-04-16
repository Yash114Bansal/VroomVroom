from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class BasePermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):

        if request.user.is_authenticated and not request.user.email_verified:
            raise PermissionDenied("Your email is not verified.")
        if request.user.is_authenticated and not request.user.phone_verified:
            raise PermissionDenied("Your phone is not verified.")
        return super().has_permission(request, view)


class IsDriver(BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.verified_driver
