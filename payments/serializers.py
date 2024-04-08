from rest_framework import serializers
from rides.models import RideModel
from .models import PassengerPayment

class PendingPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideModel
        fields = ["id","fare","departure_time"]
        
class PassengerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerPayment
        fields = '__all__'