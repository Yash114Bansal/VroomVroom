from rest_framework.generics import UpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import BasePermission
from .serializers import FCMTokenUpdateSerializer, EmailSubscriptionUpdateSerializer

class FCMTokenUpdateView(UpdateAPIView):
    """
    Update FCM Token.
    
    API Endpoint To Change FCM Token.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [BasePermission]
    serializer_class = FCMTokenUpdateSerializer

    def get_object(self):
        return self.request.user

class EmailSubscriptionUpdateView(UpdateAPIView):
    """
    Update Email Subscription Status.
    
    API Endpoint To Change Email Subscription Status.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [BasePermission]
    serializer_class = EmailSubscriptionUpdateSerializer

    def get_object(self):
        return self.request.user