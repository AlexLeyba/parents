from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from users.models import CustomUser


class Author(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    position = models.CharField("Должность", max_length=100, default="")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Tag(models.Model):
    title = models.CharField("Название", max_length=30)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField("Название", max_length=60)
    image = models.ImageField("Картинка", upload_to="images/", blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_articles_count(self):
        return self.articles.count()

    def get_videos_count(self):
        return self.videos.count()


class Step(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    number = models.SmallIntegerField("Порядковый номер шага", blank=True, null=True)

    class Meta:
        verbose_name = "Шаг для рекомендаций статей"
        verbose_name_plural = "Шаги для рекомендаций статей"

    def __str__(self):
        return self.title


class StepTag(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    step = models.ForeignKey(
        Step, on_delete=models.CASCADE, verbose_name="Шаг", related_name="step_tags"
    )

    class Meta:
        verbose_name = "Тег для шагов рекомендаций"
        verbose_name_plural = "Теги для шагов рекомендаций"

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    annotation = models.TextField("Краткая аннотация", blank=True, null=True)
    description = RichTextUploadingField("Вступительная часть")
    text = RichTextUploadingField("Тело статьи")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name="Автор статьи",
        related_name="author_articles",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Категория",
        related_name="articles",
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Тэги (в том числе и для поисковых систем)",
        related_name="article_tags",
    )
    step_tags = models.ManyToManyField(
        StepTag,
        verbose_name="Тэги для раздела 'шаги рекоменаций'",
        related_name="article_step_tags",
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title

    def get_author_name(self) -> str:
        if self.author:
            return self.author.user.email
        else:
            return ""


class Gallery(models.Model):
    image = models.ImageField("Картинка", upload_to="images/")
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name="Статья", related_name="images"
    )

    class Meta:
        verbose_name = "Картинку для слайдера"
        verbose_name_plural = "Картинки для слайдера"

    def __str__(self):
        return self.article.title


class MetaTags(models.Model):
    desc = models.TextField("Описание")
    words = models.TextField("Ключевые слова")
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        verbose_name="Статья",
        related_name="meta_tags",
    )

    class Meta:
        verbose_name = "Мета тэги для поисковых систем"
        verbose_name_plural = "Мета тэги для поисковых систем"

    def __str__(self):
        return self.article.title


class Video(models.Model):
    title = models.CharField("Название", max_length=50, default="")
    url = RichTextUploadingField("Вставьте видео сюда")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="videos",
    )

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def __str__(self):
        return self.title
