from django.urls import path

from .views import AddConsultation, CentersView, MapTagsView, StatusList

urlpatterns: list = [
    path("status-list/", StatusList.as_view()),
    path("create-consultation/", AddConsultation.as_view()),
    path("map_tags/", MapTagsView.as_view()),
    path("centers/", CentersView.as_view()),
]
