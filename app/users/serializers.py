from rest_framework import serializers

from .models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["image", "first_name", "last_name", "surname", "email"]
