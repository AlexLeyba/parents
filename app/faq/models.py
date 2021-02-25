from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class FAQ(models.Model):
    question = models.TextField("Вопрос", max_length=1500)
    answer = RichTextUploadingField("Ответ")
    check = models.BooleanField("Часто задаваемый вопрос", default=False)

    class Meta:
        verbose_name = "Вопрос - Ответ"
        verbose_name_plural = "Вопрос - Ответ"

    def __str__(self):
        return self.question


class Question(models.Model):
    name = models.CharField("ФИО", max_length=60)
    email = models.EmailField()
    text = models.TextField("Текст вопроса")

    class Meta:
        verbose_name = "Вопрос пользователя"
        verbose_name_plural = "Вопросы пользователей"

    def __str__(self):
        return self.text


class AboutUs(models.Model):
    char = models.CharField("Буква", max_length=10)
    description = models.CharField("Фраза к букве", max_length=455)

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"

    def __str__(self):
        return self.char


class UsefulLinks(models.Model):
    image = models.ImageField("картинка", upload_to="images/", blank=True, null=True)
    url = models.URLField("ссылка")

    class Meta:
        verbose_name = "Полезную ссылку"
        verbose_name_plural = "Полезные ссылки"

    def __str__(self):
        return self.url
