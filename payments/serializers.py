from rest_framework import serializers
from rides.models import RideModel


class PendingPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideModel
        fields = ["id","fare","departure_time"]