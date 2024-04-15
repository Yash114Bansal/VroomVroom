from rest_framework import serializers
from .models import UserProfile

# Serializer for updating FCM Token
class FCMTokenUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("fcm_token",)

# Serializer for updating Email Subscription
class EmailSubscriptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("subscribed_to_email",)

# Serializer for getting FCM Token and Name for Sending Push Notifications
class UserFCMSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("name", "fcm_token")
