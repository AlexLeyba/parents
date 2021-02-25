from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import (
    Book,
    Comment,
    Day,
    Film,
    Info,
    Like,
    Methodology,
    PartOfDay,
    Workshop,
)
from .serializers import (
    AddCommentSerializer,
    AddLikeSerializer,
    BookSerializer,
    DaySerializer,
    FilmSerializer,
    InfoSerializer,
    MethodologySerializer,
    PartOfDaySerializer,
    WorkshopMainSerializer,
)


class DaysViewApi(ModelViewSet):
    queryset = Day.objects.filter(publish=True)
    serializer_class = DaySerializer


class WorkshopList(ListAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopMainSerializer


class MethodologyView(ListAPIView):
    queryset = Methodology.objects.all()
    serializer_class = MethodologySerializer


class FilmView(ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


class BookView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CreateCommentBase(CreateAPIView):
    """базовый класс для реализации добавления комментариев"""

    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = AddCommentSerializer
    obj = None  # use model objects for creating comment

    def perform_create(self, serializer):
        obj = self.obj.objects.get(id=self.kwargs["pk"])
        content_type = ContentType.objects.get_for_model(obj)
        serializer.save(
            content_type=content_type, object_id=obj.id, user=self.request.user
        )


class CreateCommentForDay(CreateCommentBase):
    obj = Day


class CreateReplayToComment(CreateCommentBase):
    obj = Comment


class CreateLikeBase(APIView):
    """базовый класс для реализации добавления лайков"""

    permission_classes = [IsAuthenticated]
    obj = None  # use model objects for creating like

    def post(self, request, pk):
        obj = self.obj.objects.get(id=pk)
        content_type = ContentType.objects.get_for_model(obj)
        if Like.objects.filter(
            user=request.user, content_type_id=content_type.id, object_id=obj.id
        ).exists():
            like = Like.objects.get(
                user=request.user, content_type_id=content_type.id, object_id=obj.id
            )
            if str(like.status) == request.POST.get("status"):
                like.delete()
                return Response(
                    status=status.HTTP_204_NO_CONTENT, data={"message": "mark deleted"}
                )
            else:
                like.status = request.POST.get("status")
                like.save()
                return Response(status=status.HTTP_200_OK, data={"message": "changed"})
        else:
            Like.objects.create(
                user=request.user,
                content_type_id=content_type.id,
                object_id=obj.id,
                status=request.POST.get("status"),
            )
            return Response(status=status.HTTP_201_CREATED, data={"message": "created"})


class CreateDayLike(CreateLikeBase):
    obj = Day


class CreateCommentLike(CreateLikeBase):
    obj = Comment


class PartOfDayView(RetrieveAPIView):
    queryset = PartOfDay.objects.all()
    serializer_class = PartOfDaySerializer


class InfoView(ListAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
