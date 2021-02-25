from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    BookView,
    CreateCommentForDay,
    CreateCommentLike,
    CreateDayLike,
    CreateReplayToComment,
    DaysViewApi,
    FilmView,
    InfoView,
    MethodologyView,
    PartOfDayView,
    WorkshopList,
)

urlpatterns = format_suffix_patterns(
    [
        path("", WorkshopList.as_view()),
        path("days/<int:pk>/", DaysViewApi.as_view({"get": "retrieve"})),
        path("days/", DaysViewApi.as_view({"get": "list"})),
        path("part/<int:pk>/", PartOfDayView.as_view()),
        path("methodology/", MethodologyView.as_view()),
        path("film/", FilmView.as_view()),
        path("book/", BookView.as_view()),
        path("add-day-comment/<int:pk>/", CreateCommentForDay.as_view()),
        path("add-replay-to-comment/<int:pk>/", CreateReplayToComment.as_view()),
        path("create-day-like/<int:pk>/", CreateDayLike.as_view()),
        path("create-comment-like/<int:pk>/", CreateCommentLike.as_view()),
        path("info/", InfoView.as_view()),
    ]
)
