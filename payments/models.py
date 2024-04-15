from django.db import models
from accounts.models import UserProfile
from rides.models import RideModel

class PassengerPayment(models.Model):
    ride = models.ForeignKey(RideModel, on_delete=models.CASCADE)
    passenger = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    cash_payment_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'Payment for Ride {self.ride.id} by {self.passenger.username}'
