from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Category, Step, Video
from .serializers import (
    AlphabetVideoSerializer,
    ArticleDetailSerializer,
    ArticleSerializer,
    CategorySerializer,
    SearchArticleSerializer,
    StepsSerializer,
)


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticleDetailView(APIView):
    @staticmethod
    def get(request, pk):
        article = Article.objects.get(id=pk)
        interesting = (
            Article.objects.filter(category=article.category)
            .exclude(id=article.id)
            .order_by("?")[:3]
        )
        response = {
            "article": ArticleDetailSerializer(article).data,
            "interesting": ArticleSerializer(interesting, many=True).data,
        }
        return Response(response, status=status.HTTP_200_OK)


class SearchView(APIView):
    """поиск по сайту, формат урла /alphabet/search/?search=some_text"""

    def get(self, request):
        if self.request.GET.get("search"):
            search = self.request.GET.get("search")
            articles = Article.objects.filter(title__icontains=search)
            videos = Video.objects.filter(title__icontains=search)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "articles": SearchArticleSerializer(articles, many=True).data,
                    "videos": AlphabetVideoSerializer(videos, many=True).data,
                    "articles_count": articles.count(),
                    "videos_count": videos.count(),
                },
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LastFiveArticlesView(ListAPIView):
    """пять последних статей"""

    queryset = Article.objects.order_by("-id")[:5]
    serializer_class = ArticleSerializer


class StepsView(ListAPIView):
    """все шаги с тегами"""

    queryset = Step.objects.order_by("number")
    serializer_class = StepsSerializer


class SortedArticlesView(APIView):
    """post запрос со списком id тегов шагов {"step_tags": [some_list]}"""

    def post(self, request):
        step_tags = self.request.POST.get("step_tags")
        articles = []
        for step_tag in step_tags:
            articles.append(Article.objects.get(step_tags=step_tag))
        set(articles)
        return Response(
            ArticleSerializer(articles, many=True).data, status=status.HTTP_200_OK
        )
