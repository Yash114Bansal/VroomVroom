from rest_framework import serializers
from accounts.models import UserProfile

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["email",'name',"phone_number","profile_picture","age","gender","email_verified","phone_verified","is_staff","fcm_token","subscribed_to_email"]

class UserDetailsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["name","age","gender"]
