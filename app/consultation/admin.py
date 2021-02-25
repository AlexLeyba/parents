from django.contrib import admin

from .models import Consultation, ConsultationCenter, MapTag, Status, Theme


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ("name", "check")


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(MapTag)
class MapTagAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(ConsultationCenter)
class ConsultationCenterAdmin(admin.ModelAdmin):
    list_display = ("title",)
