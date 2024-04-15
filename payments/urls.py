from django.urls import path
from .views import PendingPaymentsListView, PassengerPaymentRequestView, DriverPaymentRequestApprovalView, DriverPaymentRequestListView

urlpatterns = [
    path('pending/', PendingPaymentsListView.as_view(), name='pending-payments-list'),
    path('request-payment/<int:ride_id>', PassengerPaymentRequestView.as_view(), name='passenger_payment_request'),
    path('list-approve-payments/', DriverPaymentRequestListView.as_view(), name='driver_payment_requests_list'),
    path('approve-payment/<int:ride_id>/', DriverPaymentRequestApprovalView.as_view(), name='approve_payment_request'),

]
