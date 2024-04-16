from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RideViewSet, RideSearchView, RideBookingView, MyRideView, MyPastRideListView, MyPastRideRetrieveView

router = DefaultRouter()
router.register(r'', RideViewSet, basename='ride')

urlpatterns = [
    path('search/',RideSearchView.as_view()),
    path('book/<int:ride_id>/', RideBookingView.as_view(), name='ride-book'),
    path('my-ride/', MyRideView.as_view(), name='ride-upcoming'),
    path('my-ride/pasts/', MyPastRideListView.as_view(), name='ride-past'),
    path('my-ride/pasts/<int:pk>/', MyPastRideRetrieveView.as_view(), name='my_past_ride_detail'),

    path('', include(router.urls)),
]