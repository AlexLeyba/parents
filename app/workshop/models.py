from datetime import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser

from .tasks import to_publish_task


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField("ID объекта")
    content_object = GenericForeignKey("content_type", "object_id")
    status = models.BooleanField("Лайк/дизлайк", default=True)

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return self.user.email


class Comment(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField("Текст комментария", max_length=1000)
    date = models.DateField("Дата", auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField("ID объекта")
    content_object = GenericForeignKey("content_type", "object_id")
    likes = GenericRelation(Like, related_name="comment_likes")
    parent_comment = models.ForeignKey(
        "self",
        verbose_name="Ответ на комментарий",
        related_name="replies",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-id"]

    def __str__(self):
        return self.user.email

    def get_likes_count(self):
        return self.likes.filter(status=True).count()

    def get_dislikes_count(self):
        return self.likes.filter(status=False).count()


class Workshop(models.Model):
    title = models.CharField("Мастерская", max_length=255)

    class Meta:
        verbose_name = "Мастерскую"
        verbose_name_plural = "Мастерские"

    def __str__(self):
        return self.title


class Day(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    number = models.SmallIntegerField("Порядковый номер дня", blank=True, null=True)
    desc = models.CharField("Краткая аннотация", max_length=355)
    image = models.ImageField("Картинка", upload_to="images/")
    video_quantity = models.SmallIntegerField("Количество видео", blank=True, null=True)
    challenge_quantity = models.SmallIntegerField(
        "Количество челленджей", blank=True, null=True
    )
    lifehack_quantity = models.SmallIntegerField(
        "Количество лайфхаков", blank=True, null=True
    )
    publish = models.BooleanField("Опубликовать день", default=False)
    publish_date = models.DateTimeField(
        "Дата и время отложенной публикации", blank=True, null=True
    )
    comment = GenericRelation(Comment, related_name="day_comments")
    likes = GenericRelation(Like, related_name="day_likes")

    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
        verbose_name="мастерская",
        related_name="days",
    )

    class Meta:
        verbose_name = "День"
        verbose_name_plural = "Дни"
        ordering = ["-number"]

    def __str__(self):
        return self.title

    def get_comments_count(self):
        return self.comment.count()

    def get_likes_count(self):
        return self.likes.filter(status=True).count()

    def get_dislikes_count(self):
        return self.likes.filter(status=False).count()


@receiver(post_save, sender=Day)
def activate_to_publish_task(instance, created, **kwargs):
    if created:
        day = instance
        if day.publish_date:
            to_publish_task.apply_async([day.id], eta=day.publish_date)


class Base(models.Model):
    title = models.CharField("Заголовок", max_length=1000)
    url = models.URLField("ссылка", blank=True, null=True)
    description = models.TextField("Описание", max_length=3000, blank=True, null=True)
    image = models.ImageField("Картинка", upload_to="images/", blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Methodology(Base):
    day = models.ForeignKey(
        Day,
        on_delete=models.CASCADE,
        verbose_name="день (не обязательно)",
        related_name="methodologies",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Методику"
        verbose_name_plural = "Методики"


class Film(Base):
    day = models.ForeignKey(
        Day,
        on_delete=models.CASCADE,
        verbose_name="день (не обязательно)",
        related_name="films",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class Book(Base):
    day = models.ForeignKey(
        Day,
        on_delete=models.CASCADE,
        verbose_name="день (не обязательно)",
        related_name="books",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Книгу"
        verbose_name_plural = "Книги"


class PartOfDay(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    text = RichTextUploadingField("Текст")
    day = models.ForeignKey(
        Day, verbose_name="День", on_delete=models.CASCADE, related_name="parts"
    )

    class Meta:
        verbose_name = "Часть дня"
        verbose_name_plural = "Части дня"

    def __str__(self):
        return self.title


class Video(models.Model):
    url = models.URLField("ссылка")
    part_day = models.ForeignKey(
        PartOfDay,
        on_delete=models.CASCADE,
        verbose_name="Часть дня",
        related_name="videos",
    )
    like = GenericRelation(Like, related_name="video_likes")

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def __str__(self):
        return self.url

    def get_likes_count(self):
        return self.like.filter(status=True).count()

    def get_dislikes_count(self):
        return self.like.filter(status=False).count()


class Image(models.Model):
    image = models.ImageField("Картинка", upload_to="images/")
    part_day = models.ForeignKey(
        PartOfDay,
        on_delete=models.CASCADE,
        verbose_name="Часть дня",
        related_name="images",
    )

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"

    def __str__(self):
        return str(self.image)


class Info(models.Model):
    title = models.CharField("Информация об мастерской", max_length=355)

    class Meta:
        verbose_name = "Информация об мастерской"
        verbose_name_plural = "Информация об мастерской"

    def __str__(self):
        return self.title
