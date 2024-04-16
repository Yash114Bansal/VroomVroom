from rest_framework import serializers
from .models import AadharCardModel, DrivingLicenseModel, ImageWithVehicleModel

# Serializer for uploading Aadhar card documents
class AadharUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AadharCardModel
        fields = ["document"]

# Serializer for uploading driving license documents
class DrivingLicenseUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivingLicenseModel
        fields = ["document"]

# Serializer for uploading images with vehicle information
class ImageWithVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageWithVehicleModel
        fields = ["document", "vehicle_type", "plate_number", "vehicle_model"]

# Serializer for retrieving Aadhar card verification status
class AadharStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AadharCardModel
        fields = ["id", "is_verified", "message"]

# Serializer for retrieving driving license verification status
class DrivingLicenseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivingLicenseModel
        fields = ["id", "is_verified", "message"]

# Serializer for retrieving image with vehicle verification status
class ImageWithVehicleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageWithVehicleModel
        fields = ["id", "is_verified", "message"]
