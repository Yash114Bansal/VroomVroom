from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import RideModel
from .permissions import PendingPaymentPermission
from .serializers import (
    MyRideSerializer,
    RideSearchSerializer,
    RideSerializer,
    RideViewSerializer,
)
from accounts.permissions import IsDriver, BasePermission
from accounts.tasks import send_push_notification
from accounts.serializers import UserFCMSerializer



class RideViewSet(viewsets.ModelViewSet):
    """
    Create, Update, Delete Rides.

    API Endpoint For Drivers to Create, Read ,Update, Delete Rides.
    """

    queryset = RideModel.objects.all()
    serializer_class = RideSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsDriver]

    def get_queryset(self):
        return RideModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if RideModel.objects.filter(user=user).exists():
            return Response(
                {"error": "You already have an active ride."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user != instance.user:
            return Response(
                {"error": "You do not have permission to delete this ride."},
                status=status.HTTP_403_FORBIDDEN,
            )

        user_details = UserFCMSerializer(instance.passengers.all(), many=True).data
        send_push_notification.delay(
            title="Ride Cancelled!!!!",
            body=r"Dear {name}, We are sorry to inform you, your ride has been cancelled by Captain.",
            users=user_details,
        )

        self.perform_destroy(instance)
        return Response(
            {"message": "Ride successfully deleted."}, status=status.HTTP_204_NO_CONTENT
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user_details = UserFCMSerializer(instance.passengers.all(), many=True).data
        send_push_notification.delay(
            title="Ride Updated!!!!",
            body=r"Hey {name}, Your ride is updated, open the app to view changes",
            users=user_details,
        )
        return super().update(request, *args, **kwargs)


class RideSearchView(GenericAPIView):
    """
    Search Rides.

    API Endpoint to Search For Rides.
    """

    serializer_class = RideSearchSerializer
    permission_classes = [BasePermission, PendingPaymentPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "departure_offset",
                openapi.IN_QUERY,
                description="",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "destination_offset",
                openapi.IN_QUERY,
                description="",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "departure_time_start",
                openapi.IN_QUERY,
                description="",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "departure_time_end",
                openapi.IN_QUERY,
                description="",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pickup_location = serializer.validated_data["pickup_location"]
        destination_location = serializer.validated_data["destination_location"]

        # Get departure and destination offset distances from query parameters
        departure_offset = request.query_params.get("departure_offset")
        destination_offset = request.query_params.get("destination_offset")

        # Get departure datetime range from query parameters
        departure_time_start = request.query_params.get("departure_time_start")
        departure_time_end = request.query_params.get("departure_time_end")

        # Apply filters only if offset distances are provided
        rides_within_offset = RideModel.objects.filter(status="upcoming")
        if departure_offset:
            rides_within_offset = rides_within_offset.filter(
                departure_location__distance_lte=(pickup_location, departure_offset)
            )
        if destination_offset:
            rides_within_offset = rides_within_offset.filter(
                destination_location__distance_lte=(
                    destination_location,
                    destination_offset,
                )
            )

        if departure_time_start and departure_time_end:
            rides_within_offset = rides_within_offset.filter(
                departure_time__range=(departure_time_start, departure_time_end)
            )

        rides_within_offset = rides_within_offset.annotate(
            departure_distance=Distance(
                "departure_location", GEOSGeometry(pickup_location, srid=4326)
            ),
            destination_distance=Distance(
                "destination_location", GEOSGeometry(destination_location, srid=4326)
            ),
        )
        page = self.paginate_queryset(rides_within_offset)

        if page is not None:
            rides_within_offset_data = RideViewSerializer(page, many=True).data
            return self.get_paginated_response(rides_within_offset_data)

        rides_within_offset_data = RideViewSerializer(
            rides_within_offset, many=True
        ).data

        return Response(rides_within_offset_data, status=status.HTTP_200_OK)


class RideBookingView(APIView):
    """
    Book Ride.

    API Endpoint To Book the Ride.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [BasePermission, PendingPaymentPermission]

    def post(self, request, ride_id, *args, **kwargs):
        try:
            ride = RideModel.objects.get(id=ride_id)
        except RideModel.DoesNotExist:
            return Response(
                {"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user = self.request.user

        if ride.user == user:
            return Response(
                {"error": "You cannot book your own ride"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user in ride.passengers.all():
            return Response(
                {"error": "You have already booked this ride"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if ride.status != "upcoming":
            return Response(
                {"error": "Ride is not available"}, status=status.HTTP_400_BAD_REQUEST
            )

        if ride.seat_available <= 0:
            return Response(
                {"error": "No available seats in this ride"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ride.passengers.add(user)
        ride.seat_available -= 1
        ride.save()

        return Response(
            {"message": "Ride successfully booked"}, status=status.HTTP_200_OK
        )


class MyRideView(ListAPIView):
    """
    Get Current Ride.

    API Endpoint To Get Details of Current Ride.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [BasePermission]
    serializer_class = MyRideSerializer

    def get_queryset(self):
        return RideModel.objects.filter(
            passengers=self.request.user, status__in=["upcoming", "onway"]
        )


class MyPastRideListView(ListAPIView):
    """
    Get Past Rides.

    API Endpoint To Get Details of Past Rides.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [BasePermission]
    serializer_class = MyRideSerializer

    def get_queryset(self):
        return RideModel.objects.filter(
            passengers=self.request.user, status="completed"
        )


class MyPastRideRetrieveView(RetrieveAPIView):
    """
    Get Past Ride.

    API Endpoint To Get Details of a Past Ride.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [BasePermission]
    serializer_class = MyRideSerializer

    def get_queryset(self):
        return RideModel.objects.filter(
            passengers=self.request.user, status="completed"
        )
