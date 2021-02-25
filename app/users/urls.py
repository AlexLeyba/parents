from django.urls import path

from .views import ProfileView, reset_user_password

urlpatterns: list = [
    path("profile/<int:pk>/", ProfileView.as_view()),
    path("reset/<slug:uid>/<slug:token>/", reset_user_password, name="reset"),
]
