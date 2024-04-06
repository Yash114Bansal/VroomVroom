from django.urls import path
from .views import FCMTokenUpdateView, EmailSubscriptionUpdateView

urlpatterns = [
    path('fcm-token/', FCMTokenUpdateView.as_view(), name='fcm_token_update'),
    path('email-subscription/', EmailSubscriptionUpdateView.as_view(), name='email-subscription-update'),
]
