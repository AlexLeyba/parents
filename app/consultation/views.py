from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView, Response

from .models import Consultation, ConsultationCenter, MapTag, Status, Theme
from .serializers import (
    ConsultationCenterSerializer,
    ConsultationSerializer,
    MapTagSerializer,
    StatusSerializer,
    ThemeSerializer,
)


class AddConsultation(CreateAPIView):
    """создание консультации"""

    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer


class StatusList(APIView):
    """вывод списка тем, статусов для формы консультации"""

    def get(self, request):
        statuses = Status.objects.all()
        themes = Theme.objects.all()
        return Response(
            status=status.HTTP_200_OK,
            data={
                "statuses": StatusSerializer(statuses, many=True).data,
                "themes": ThemeSerializer(themes, many=True).data,
            },
        )


class MapTagsView(ListAPIView):
    """консультации на карте"""

    queryset = MapTag.objects.all()
    serializer_class = MapTagSerializer


class CentersView(ListAPIView):
    """список центров консультаций"""

    queryset = ConsultationCenter.objects.all()
    serializer_class = ConsultationCenterSerializer
