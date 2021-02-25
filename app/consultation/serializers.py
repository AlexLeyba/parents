from rest_framework import serializers

from .models import Consultation, ConsultationCenter, MapTag, Status, Theme


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = "__all__"


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = "__all__"


class MapTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapTag
        fields = "__all__"


class ConsultationCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationCenter
        fields = "__all__"
