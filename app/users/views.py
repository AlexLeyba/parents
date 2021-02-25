import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializers import ProfileSerializer


class ProfileView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer


def reset_user_password(request, uid, token):
    if request.method == "POST":
        password = request.POST.get("password1")
        payload = {"uid": uid, "token": token, "new_password": password}
        url = "https://back-parents.admlr.lipetsk.ru/auth/users/reset_password_confirm/"
        response = requests.post(url, data=payload)
        if response.status_code == 204:
            return HttpResponseRedirect("http://roditel48.ru/?login=true")
        else:
            return Response({"error": "не корректные данные"})
    if request.method == "GET":
        return render(request, "reset_password.html", {"uid": uid, "token": token})
