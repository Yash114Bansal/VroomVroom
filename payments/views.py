from rest_framework import generics
from accounts.permissions import BasePermission
from rides.models import RideModel
from .serializers import PendingPaymentsSerializer

class PendingPaymentsListView(generics.ListAPIView):
    serializer_class = PendingPaymentsSerializer
    permission_classes = [BasePermission]

    def get_queryset(self):
        user = self.request.user  
        queryset = RideModel.objects.filter(passengers=user).exclude(paid_by=user)
        return queryset
