from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from .models import PassengerPayment
from rides.models import RideModel

User = get_user_model()

class PaymentTestCase(APITestCase):
    def setUp(self):
        self.driver = User.objects.create(email='test@example.com',name = "Bansal",password="testpassword",email_verified=True,phone_verified=True)

        self.passenger = User.objects.create(email='test2@example.com',password="test2password",email_verified=True,phone_verified=True)
        self.ride = RideModel.objects.create(user=self.driver, seat_available=2,departure_location="POINT (-74.0059 40.7128)", destination_location="POINT (-74.0059 40.7128)",departure_time="2024-01-30T12:00:00Z",fare=21.0,status="completed")

        self.ride.passengers.add(self.passenger)
        self.passenger_token = AccessToken.for_user(self.passenger)
        self.driver_token = AccessToken.for_user(self.driver)

    def test_pending_payments_list(self):
        url = reverse('pending-payments-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.passenger_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], RideModel.objects.filter(passengers=self.passenger).exclude(paid_by=self.passenger).count())

    def test_passenger_payment_request(self):
        url = reverse('passenger_payment_request', kwargs={'ride_id': self.ride.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.passenger_token}')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PassengerPayment.objects.filter(ride=self.ride, passenger=self.passenger).exists())

    def test_driver_payment_request_list(self):
        url = reverse('driver_payment_requests_list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.driver_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], PassengerPayment.objects.filter(ride__user=self.driver, cash_payment_verified=False).count())

    def test_driver_payment_request_approval(self):
        payment = PassengerPayment.objects.create(ride=self.ride, passenger=self.passenger)
        url = reverse('approve_payment_request', kwargs={'ride_id': self.ride.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.driver_token}')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment.refresh_from_db()
        self.assertTrue(payment.cash_payment_verified)
