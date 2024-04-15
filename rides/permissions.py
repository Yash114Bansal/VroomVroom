from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import RideModel

class PendingPaymentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        completed_rides_with_pending_payment = RideModel.objects.filter(
            passengers=request.user,
            status='completed'
        ).exclude(paid_by=request.user)
        
        if completed_rides_with_pending_payment.exists():
            raise PermissionDenied("You have pending payments for completed rides.")
        return True
