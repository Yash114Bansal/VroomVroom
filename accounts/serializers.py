from rest_framework import serializers
from .models import UserProfile

class FCMTokenUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('fcm_token',)

class EmailSubscriptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('subscribed_to_email',)
