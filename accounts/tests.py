from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import UserProfile


class FCMTokenUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            email="test@example.com",
            password="testpassword",
            email_verified=True,
            phone_verified=True,
        )
        self.client = APIClient()

    def test_update_fcm_token_authenticated(self):
        # Verifying Token Updation
        self.client.force_authenticate(user=self.user)
        new_token = "new_token"
        response = self.client.put(
            reverse("fcm_token_update"), {"fcm_token": new_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user = UserProfile.objects.get(email=self.user.email)
        self.assertEqual(self.user.fcm_token, new_token)

    def test_update_fcm_token_unauthenticated(self):
        new_token = "new_token"
        response = self.client.put(
            reverse("fcm_token_update"), {"fcm_token": new_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(self.user.fcm_token, new_token)


class EmailSubscriptionUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            email="test@example.com",
            password="testpassword",
            email_verified=True,
            phone_verified=True,
        )
        self.client = APIClient()

    def test_update_email_subscription_authenticated(self):
        self.client.force_authenticate(user=self.user)
        new_subscription_status = False
        response = self.client.put(
            reverse("email-subscription-update"),
            {"subscribed_to_email": new_subscription_status},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.subscribed_to_email, new_subscription_status)

    def test_update_email_subscription_unauthenticated(self):
        new_subscription_status = False
        response = self.client.put(
            reverse("email-subscription-update"),
            {"subscribed_to_email": new_subscription_status},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.subscribed_to_email, new_subscription_status)
