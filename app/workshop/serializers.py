from rest_framework import serializers

from users.models import CustomUser

from .models import (
    Book,
    Comment,
    Day,
    Film,
    Image,
    Info,
    Like,
    Methodology,
    PartOfDay,
    Video,
    Workshop,
)


class WorkshopMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ("id", "title")


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["image", "first_name", "surname", "email"]


class ParentCommentSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source="get_likes_count")
    dislikes = serializers.IntegerField(source="get_dislikes_count")
    user = CustomUserSerializer()

    class Meta:
        model = Comment
        fields = ("id", "user", "text", "date", "likes", "dislikes")


class CommentSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source="get_likes_count")
    dislikes = serializers.IntegerField(source="get_dislikes_count")
    user = CustomUserSerializer()
    replies = ParentCommentSerializer(many=True)

    class Meta:
        model = Comment
        fields = ("id", "user", "text", "date", "likes", "dislikes", "replies")


class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("text", "parent_comment")


class AddLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "user", "content_type", "object_id", "status")


class VideoSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source="get_likes_count")
    dislikes = serializers.IntegerField(source="get_dislikes_count")

    class Meta:
        model = Video
        fields = ("id", "url", "part_day", "likes", "dislikes")


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "image", "part_day")


class PartOfDaySerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = PartOfDay
        fields = ("id", "title", "text", "day", "videos", "images")


class MethodologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Methodology
        fields = ("id", "title", "url", "description", "image", "day")


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ("id", "title", "url", "description", "image", "day")


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "url", "description", "image", "day")


class DaySerializer(serializers.ModelSerializer):
    parts = PartOfDaySerializer(many=True, required=False)
    methodologies = MethodologySerializer(many=True, required=False)
    films = FilmSerializer(many=True, required=False)
    books = BookSerializer(many=True, required=False)
    comment = CommentSerializer(many=True)
    comments_count = serializers.IntegerField(source="get_comments_count")
    likes = serializers.IntegerField(source="get_likes_count")
    dislikes = serializers.IntegerField(source="get_dislikes_count")

    class Meta:
        model = Day
        fields = (
            "id",
            "number",
            "title",
            "desc",
            "image",
            "parts",
            "methodologies",
            "films",
            "books",
            "video_quantity",
            "challenge_quantity",
            "lifehack_quantity",
            "workshop",
            "comment",
            "comments_count",
            "likes",
            "dislikes",
        )


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = "__all__"
