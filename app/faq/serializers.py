from rest_framework import serializers

from .models import FAQ, AboutUs, Question, UsefulLinks


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ("id", "question", "answer")


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "name", "email", "text")


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"


class UsefulLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsefulLinks
        fields = "__all__"
