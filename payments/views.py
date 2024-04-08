from django.shortcuts import get_object_or_404
from rest_framework import generics
from accounts.permissions import BasePermission
from rides.models import RideModel
from .serializers import PassengerPaymentSerializer, PendingPaymentsSerializer
from rest_framework.response import Response
from .models import PassengerPayment
from rest_framework import status
from rest_framework.views import APIView
from accounts.tasks import send_push_notification
from accounts.serializers import UserFCMSerializer

class PendingPaymentsListView(generics.ListAPIView):
    serializer_class = PendingPaymentsSerializer
    permission_classes = [BasePermission]

    def get_queryset(self):
        user = self.request.user  
        queryset = RideModel.objects.filter(passengers=user).exclude(paid_by=user)
        return queryset

class PassengerPaymentRequestView(generics.CreateAPIView):
    
    def create(self, request, ride_id,*args, **kwargs):
        # ride_id = request.data.get('')
        passenger = request.user
        
        print("Hiii Ride ID is ", ride_id)
        ride = get_object_or_404(RideModel, id=ride_id)
        print(ride)
        if ride.status == 'upcoming':
            return Response({'message': 'Cannot request payment for upcoming ride.'}, status=status.HTTP_400_BAD_REQUEST)
        if passenger not in ride.passengers.all():
            return Response({'message': 'Passenger is not part of this ride.'}, status=status.HTTP_400_BAD_REQUEST)
        if passenger in ride.paid_by.all():
            return Response({'message': 'Payment already made for this ride.'}, status=status.HTTP_400_BAD_REQUEST)

        if PassengerPayment.objects.filter(ride=ride, passenger=passenger).exists():
            return Response({'message': 'Payment request already exists for this ride.'}, status=status.HTTP_400_BAD_REQUEST)

        PassengerPayment.objects.create(
            ride=ride,
            passenger=passenger,
            cash_payment_verified=False
        )
        user_details = UserFCMSerializer([ride.user], many=True).data

        send_push_notification.delay(title="Payment Request.",body=r"Dear {name}, "+f"{passenger.name} has requested to record cash payment for ride.",users=user_details)
        return Response({'message': 'Passenger payment request created successfully.'}, status=status.HTTP_201_CREATED)

class DriverPaymentRequestListView(generics.ListAPIView):
    serializer_class = PassengerPaymentSerializer

    def get_queryset(self):
        driver = self.request.user
        return PassengerPayment.objects.filter(ride__user=driver, cash_payment_verified=False)

class DriverPaymentRequestApprovalView(APIView):
    def post(self, request, ride_id, *args, **kwargs):
        try:
            payment_request = PassengerPayment.objects.get(ride__id=ride_id, cash_payment_verified=False)
        except PassengerPayment.DoesNotExist:
            return Response({'message': 'Payment request not found.'}, status=status.HTTP_404_NOT_FOUND)

        driver = request.user

        if payment_request.ride.user != driver:
            return Response({'message': 'Unauthorized: You are not the driver of this ride.'}, status=status.HTTP_403_FORBIDDEN)

        payment_request.cash_payment_verified = True
        payment_request.ride.paid_by.add(payment_request.passenger)
        payment_request.save()
        
        user_details = UserFCMSerializer([payment_request.passenger], many=True).data
        send_push_notification.delay(title="Payment Request Approved.",body=r"Dear {name}, Your Payment Request has Been Approved!.",users=user_details)

        return Response({'message': 'Payment request approved successfully.'}, status=status.HTTP_200_OK)