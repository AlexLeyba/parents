from django.urls import path

from .views import (
    ArticleDetailView,
    CategoryListView,
    LastFiveArticlesView,
    SearchView,
    SortedArticlesView,
    StepsView,
)

urlpatterns = [
    path("", CategoryListView.as_view()),
    path("article/<int:pk>/", ArticleDetailView.as_view()),
    path("search/", SearchView.as_view()),
    path("last_five_articles/", LastFiveArticlesView.as_view()),
    path("steps/", StepsView.as_view()),
    path("sorted_articles/", SortedArticlesView.as_view()),
]
