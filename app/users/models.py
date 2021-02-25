from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email"), unique=True)
    first_name = models.CharField("Имя", max_length=20, blank=True, default="")
    last_name = models.CharField("Отчество", max_length=40, blank=True, default="")
    surname = models.CharField("Фамилия", max_length=40, blank=True, default="")
    image = models.ImageField("Аватар", upload_to="avatars/", blank=True, null=True)
    is_staff = models.BooleanField("Персонал", default=False)
    is_active = models.BooleanField("Активный", default=True)
    date_joined = models.DateTimeField("Дата входа", default=timezone.now)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
