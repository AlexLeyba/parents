from rest_framework.generics import CreateAPIView, ListAPIView

from .models import FAQ, AboutUs, Question, UsefulLinks
from .serializers import (
    AboutUsSerializer,
    FAQSerializer,
    QuestionSerializer,
    UsefulLinksSerializer,
)


class FAQView(ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class QuestionView(CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class FavoriteFAQ(ListAPIView):
    queryset = FAQ.objects.filter(check=True)
    serializer_class = FAQSerializer


class AboutUsView(ListAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer


class UsefulLinksView(ListAPIView):
    queryset = UsefulLinks.objects.all()
    serializer_class = UsefulLinksSerializer
