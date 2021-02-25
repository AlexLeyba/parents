from rest_framework import serializers

from .models import Article, Category, Gallery, MetaTags, Step, StepTag, Tag, Video


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "title")


class MetaTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaTags
        fields = ["id", "desc", "words"]


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["image"]


class SearchArticleSerializer(serializers.ModelSerializer):
    images = GallerySerializer(many=True)

    class Meta:
        model = Article
        fields = ["id", "title", "annotation", "images"]


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("id", "title", "annotation", "description")


class ArticleDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author_name = serializers.CharField(source="get_author_name")
    meta_tags = MetaTagsSerializer()
    images = GallerySerializer(many=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "annotation",
            "description",
            "text",
            "author_name",
            "tags",
            "meta_tags",
            "images",
        )


class AlphabetVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("id", "title", "url")


class CategorySerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True)
    videos = AlphabetVideoSerializer(many=True)
    articles_count = serializers.IntegerField(source="get_articles_count")
    videos_count = serializers.IntegerField(source="get_videos_count")

    class Meta:
        model = Category
        fields = (
            "id",
            "title",
            "image",
            "articles_count",
            "videos_count",
            "articles",
            "videos",
        )


class StepTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepTag
        fields = ["id", "title"]


class StepsSerializer(serializers.ModelSerializer):
    step_tags = StepTagsSerializer(many=True)

    class Meta:
        model = Step
        fields = ["id", "title", "step_tags"]
