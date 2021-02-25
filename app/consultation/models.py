from smtplib import SMTPDataError

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Theme(models.Model):
    title = models.CharField("Название темы", max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Темы"
        verbose_name_plural = "Темы"


class Status(models.Model):
    title = models.CharField("Статус", max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Consultation(models.Model):
    SEX = [("Муж", "Муж"), ("Жен", "Жен")]
    AGE = [
        ("18 - 35", "18 - 35"),
        ("36 - 50", "36 - 50"),
        ("51 - 65", "51 - 65"),
        ("старше 65", "старше 65"),
    ]
    name = models.CharField("ФИО", max_length=255)
    email = models.EmailField("email", max_length=255)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    sex = models.CharField("Пол", max_length=3, choices=SEX)
    age = models.CharField("Возраст", max_length=10, choices=AGE)
    district = models.CharField("Район", max_length=255, blank=True, null=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_DEFAULT,
        verbose_name="Статус",
        related_name="consultations_on_status",
        default="",
    )
    theme = models.ForeignKey(
        Theme,
        on_delete=models.SET_DEFAULT,
        verbose_name="Тема",
        related_name="consultations_on_theme",
        default="",
    )
    check = models.BooleanField("Просмотрено", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Консультация"
        verbose_name_plural = "Консультации"


@receiver(post_save, sender=Consultation)
def send_consultation_mail(instance, created, **kwargs):
    consultations = instance
    if created:
        try:
            send_mail(
                subject=f"Новое обращение от {consultations.name} на сайте roditel48",
                message=f"Пожалуйста перейдите в административную панель сайта, и обработайте обращение",
                recipient_list=["trening@семья48.рф"],
                from_email="info-roditel48@yandex.ru",
            )
            send_mail(
                subject=f"Благодарим вас за обращение {consultations.name}",
                message=f"Скоро с вами свяжется сотрудник центра для уточнения времени",
                recipient_list=[consultations.email],
                from_email="info-roditel48@yandex.ru",
            )
        except SMTPDataError:
            pass


class MapTag(models.Model):
    title = models.CharField("Название региона", max_length=200)
    value = models.CharField("Значение", max_length=100)
    slug = models.CharField("slug", max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Консультации на карте"
        verbose_name_plural = "Консультации на карте"


class ConsultationCenter(models.Model):
    title = models.CharField("Заголовок", max_length=755)
    description = RichTextUploadingField("Описание")
    image = models.ImageField(
        "Картинка карты", upload_to="images/", blank=True, null=True
    )
    address = models.CharField("Адрес", max_length=255, blank=True, default="")
    url = models.URLField("url", blank=True, default="")
    phone = models.CharField("Телефон", max_length=255, blank=True, default="")
    email = models.EmailField("email", blank=True, default="")
    skype = models.CharField("skype", max_length=255, blank=True, default="")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Центр консультаций"
        verbose_name_plural = "Центры консультаций"
