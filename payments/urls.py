from django.urls import path
from .views import PendingPaymentsListView

urlpatterns = [
    path('pending/', PendingPaymentsListView.as_view(), name='pending-payments-list'),
]
