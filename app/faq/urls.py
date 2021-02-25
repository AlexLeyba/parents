from django.urls import path

from .views import AboutUsView, FAQView, FavoriteFAQ, QuestionView, UsefulLinksView

urlpatterns = [
    path("", FAQView.as_view()),
    path("new/", QuestionView.as_view()),
    path("favorite-faq/", FavoriteFAQ.as_view()),
    path("useful_links/", UsefulLinksView.as_view()),
    path("about_us/", AboutUsView.as_view()),
]
